# load the data into a database
# (for now, will clear and readd all the data)
import os
from query.models import WatchData 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH_DIR = os.path.join(BASE_DIR, 'anonymized_data/') # where all data and config files for data should be stored
RELOAD_DIR = os.path.join(WATCH_DIR, 'reload.txt')     # signals for a reload when not empty
reload_file = open(RELOAD_DIR, 'r')

if reload_file.readlines():
	print(f'reseting database with all data from: {WATCH_DIR}')

	# accumulate all file paths to read from
	paths = [] 
	for root, directory, files in os.walk(WATCH_DIR):
		for file in files:
			if 'watches_range.txt' in file:
				paths.append(os.path.join(root, file)) 


	# reload the database
	WatchData.objects.all().delete()
	print('database cleared')
	data_objects = []
	file_num = 0
	for path in paths:
		file_num+=1
		file = open(path, 'r')
		lines = file.readlines()
		print(f'({file_num}/{len(paths)}) reading in: {path} ({len(lines)} lines)')

		# read in data from each line
		for line in lines:
			line_entries = line.split('|')
			date = line_entries[0][0:10]
			time = line_entries[0][11: 26]
			vid_timestamp = float(line_entries[1])
			speed = float(line_entries[2])
			user_id = int(line_entries[5])
			vid_num = int(line_entries[6])

			# create object
			data_objects.append(WatchData(date=date, 
				time=time, 
				vid_timestamp=vid_timestamp, 
				speed=speed, user_id=user_id, 
				vid_num=vid_num))
	print('all objects created, saving to database')
	WatchData.objects.bulk_create(data_objects)
	print('objects saved, clearing the reload_file')
	reload_file.close()
	reload_file = open(RELOAD_DIR, 'w')
	reload_file.write('')
	reload_file.close()
reload_file.close()
print('fetch.py was run again, reload_file closed')

def get_users():
	all_watches = WatchData.objects.all()
	redundant_users = []
	for watch in all_watches:
		redundant_users.append(watch.user_id)
	return list(set(redundant_users))

def get_vids_for_user(user_id):
	all_watches = WatchData.objects.all().filter(user_id=user_id)
	redundant_vid_nums = []
	for watch in all_watches:
		redundant_vid_nums.append(watch.vid_num)
	return list(set(redundant_vid_nums))

def get_objects_by_user_vid(user_id, vid_num):
	return WatchData.objects.all().filter(user_id=user_id, vid_num=vid_num)