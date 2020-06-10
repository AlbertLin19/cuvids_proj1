# load the data into a database
# (for now, will clear and readd all the data)
import os
from query.models import WatchData 
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


paths = [os.path.join(BASE_DIR, 'watch.txt'),]
WatchData.objects.all().delete()

data_objects = []
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
	WatchData.objects.bulk_create(data_objects)





def getWatchData():
	return ["test"]

def has_user(user_id):
	return True

def user_watched_vid(user_id, vid_num):
	return True