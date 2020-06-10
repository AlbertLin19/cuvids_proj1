# load the data into a database
# (for now, will clear and readd all the data)
import os
from query.models import WatchData 
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


paths = [os.path.join(BASE_DIR, 'watch.txt'),]
WatchData.objects.all().delete()

data_objects = []
redundant_users = []
for path in paths:
	file = open(path, 'r')
	lines = file.readlines()
	for line in lines:
		line_entries = line.split('|')
		date = line_entries[0][0:10]
		time = line_entries[0][11: 26]
		vid_timestamp = float(line_entries[1])
		speed = float(line_entries[2])
		user_id = int(line_entries[5])
		vid_num = int(line_entries[6])
		data_objects.append(WatchData(date=date, 
			time=time, 
			vid_timestamp=vid_timestamp, 
			speed=speed, user_id=user_id, 
			vid_num=vid_num))
		redundant_users.append(user_id)
	WatchData.objects.bulk_create(data_objects)

users = list(set(redundant_users))

def get_users():
	return users

def get_vids_for_user(user_id):
	all_watches = WatchData.objects.all().filter(user_id=user_id)
	redundant_vid_nums = []
	for watch in all_watches:
		redundant_vid_nums.append(watch.vid_num)
	return list(set(redundant_vid_nums))

def get_objects_by_user_vid(user_id, vid_num):
	return WatchData.objects.all().filter(user_id=user_id, vid_num=vid_num)