# load the csv data into a pandas dataframe format
# (for now, will clear and readd all the data if update indicated in 'reload.txt')
import os
import pandas as pd

# the Agg needs to be used to prevent 'outside main thread error' with the 'get_watch_patten_graph()' function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH_DIR = os.path.join(BASE_DIR, 'summer_data_csv/') # where all data and config files for data should be stored
STATIC_DIR = os.path.join(BASE_DIR, 'proj1/query/static/') # where static files stored
RELOAD_DIR = os.path.join(WATCH_DIR, 'reload.txt')     # signals for a reload when not empty
reload_file = open(RELOAD_DIR, 'r')
SAVE_DIR = os.path.join(WATCH_DIR, 'pandas_watch_data.pkl') # where the pandas dataframe is saved

if reload_file.readlines():
	print(f'resetting pandas dataframes with all data from: {WATCH_DIR}')

	# accumulate all file paths to read from
	paths = [] 
	for root, directory, files in os.walk(WATCH_DIR):
		for file in files:
			if 'watch_list' in file:
				paths.append(os.path.join(root, file)) 


	# create and save the dataframe
	dataframes = []
	file_num = 0
	for path in paths:
		file_num+=1
		print(f'({file_num}/{len(paths)}) reading in: {path}')
		dataframe = pd.read_csv(path)
		print(f'shape of dataframe is {dataframe.shape}')
		dataframes.append(dataframe)

	print('dataframes for each csv file created, saving to one pandas dataframe')
	final_dataframe = dataframes[0]
	for i in range(len(dataframes)-1):
		final_dataframe = pd.concat([final_dataframe, dataframes[i+1]])
	print(f'shape of final dataframe is {final_dataframe.shape}')

	# add column for email domain
	final_dataframe['Domain'] = final_dataframe['Email'].str.split('@').str[1]

	final_dataframe.to_pickle(SAVE_DIR)
	print('final dataframe saved, clearing the reload_file')
	reload_file.close()
	reload_file = open(RELOAD_DIR, 'w')
	reload_file.write('')
	reload_file.close()

# reload script finished, close up everything
reload_file.close()
print('fetch_csv.py was run again, reload_file closed')

# load the saved pandas dataframe
print('opening the saved pandas dataframe to be used in the app')
final_dataframe = pd.read_pickle(SAVE_DIR)

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