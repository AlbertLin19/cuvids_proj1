# load the csv data into a pandas dataframe format
import pandas as pd

# the Agg needs to be used to prevent 'outside main thread error' with the 'get_watch_patten_graph()' function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime

# data stored in S3 bucket
from django.core.files.storage import default_storage
DATA_DIR = 'summer_data_csv/' # where all data and config files for data should be stored
SAVE_DIR = DATA_DIR + 'pandas_watch_data.pkl' # where the pandas dataframe is saved

users = []
videos = []
email_domains = []
# load the saved pandas dataframe if it exists
if default_storage.exists(SAVE_DIR):
	print('opening the saved pandas dataframe to initialize users, videos, email_domains')
	save_file = default_storage.open(SAVE_DIR)
	final_dataframe = pd.read_pickle(save_file)
	save_file.close()
	# cache the unique users, videos, and email domains for quicker performance
	users = final_dataframe['Username'].unique()
	videos = final_dataframe['Video Id'].unique()
	email_domains = final_dataframe['Domain'].unique()

# store the csv data from DATA_DIR into the pandas pickle file
def store_csv():
	print(f'resetting pandas dataframes with all data from: {DATA_DIR}')
	dataframes = []
	file_num = 0
	# accumulate all files to read from
	folders, files = default_storage.listdir(DATA_DIR) # files is a list of path strings
	for file in files:
		if 'watch_list' in file:
			file_num+=1
			print(f'({file_num}/{len(files)}) reading in: {file}')
			open_file = default_storage.open(DATA_DIR + file)
			dataframe = pd.read_csv(open_file)
			open_file.close()
			print(f'shape of dataframe is {dataframe.shape}')
			dataframes.append(dataframe)
	
	print('dataframes for each csv file created, merging to one pandas dataframe')
	final_dataframe = dataframes[0]
	for i in range(len(dataframes)-1):
		final_dataframe = pd.concat([final_dataframe, dataframes[i+1]])
	print(f'shape of final dataframe is {final_dataframe.shape}')

	# add column for email domain
	final_dataframe['Domain'] = final_dataframe['Email'].str.split('@').str[1]

	save_file = default_storage.open(SAVE_DIR, 'w')
	final_dataframe.to_pickle(save_file)
	save_file.close()
	print('final dataframe saved')

# recache the users, videos, and email_domains
def refresh_cache():
	# load the saved pandas dataframe
	print('opening the saved pandas dataframe to recache users, videos, email_domains')
	save_file = default_storage.open(SAVE_DIR)
	final_dataframe = pd.read_pickle(save_file)
	save_file.close()
	# cache the unique users, videos, and email domains for quicker performance
	users = final_dataframe['Username'].unique()
	videos = final_dataframe['Video Id'].unique()
	email_domains = final_dataframe['Domain'].unique()

def get_users():
	return users

def get_videos():
	return videos

def get_email_domains():
	return email_domains

# functions supporting the utilities we were asked to provide

def get_time_and_users_for_vid(video_id):
	relevant_dataframe = final_dataframe[final_dataframe['Video Id']==video_id]
	counts = len(relevant_dataframe.index)
	rel_users = relevant_dataframe['Username'].unique()
	return counts, rel_users

def get_time_and_vids_for_user(user_id):
	relevant_dataframe = final_dataframe[final_dataframe['Username']==user_id]
	counts = len(relevant_dataframe.index)
	rel_vids = relevant_dataframe['Video Id'].unique()
	return counts, rel_vids