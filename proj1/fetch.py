# load the data into a database
# (for now, will clear and readd all the data)
import os
from query.models import WatchData 

# the Agg needs to be used to prevent 'outside main thread error' with the 'get_watch_patten_graph()' function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH_DIR = os.path.join(BASE_DIR, 'anonymized_data/') # where all data and config files for data should be stored
STATIC_DIR = os.path.join(BASE_DIR, 'proj1/query/static/') # where static files stored
RELOAD_DIR = os.path.join(WATCH_DIR, 'reload.txt')     # signals for a reload when not empty
reload_file = open(RELOAD_DIR, 'r')

# cache the unique users and videos for quicker performance
users = []
videos = []

if reload_file.readlines():
	print(f'resetting database with all data from: {WATCH_DIR}')

	# accumulate all file paths to read from
	paths = [] 
	for root, directory, files in os.walk(WATCH_DIR):
		for file in files:
			if 'watches_range.txt' in file:
				paths.append(os.path.join(root, file)) 


	# reload the database
	WatchData.objects.all().delete()
	print('database cleared')
	data_objects = [] # accumulate data objects to store
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

	
# script finished, close up everything
reload_file.close()
print('fetch.py was run again, reload_file closed')

# need to recache the unique users and videos upon a rerun of this script
print("getting all the unique users and videos from the database")
users = sorted(list(set(WatchData.objects.all().values_list('user_id', flat=True))))
videos = sorted(list(set(WatchData.objects.all().values_list('vid_num', flat=True))))

def get_users():
	return users

def get_vids_for_user(user_id):
	all_watches = WatchData.objects.all().filter(user_id=user_id)
	redundant_vid_nums = []
	for watch in all_watches:
		redundant_vid_nums.append(watch.vid_num)
	return sorted(list(set(redundant_vid_nums)))

def get_watch_patten_graph(user_id, vid_num):
	gap_duration = 8 # watch is considered to be another session if gap exceeds this in seconds

	# color for speeds - red will be scaled by speed
	blue = 198/255.0
	green = 168/255.0
	alpha = 1
	max_speed = 1 # speed scaled relative to this - will be found below

	objs = WatchData.objects.all().filter(user_id=user_id, vid_num=vid_num).order_by('date', 'time')
	if len(objs) == 0:
		return None
	
	dates = []
	times = []
	timestamps = []
	speeds = []
	colors = []

	for obj in objs:
		dates.append(obj.date)
		times.append(obj.time)
		timestamps.append(obj.vid_timestamp)
		speeds.append(obj.speed)
		
		if obj.speed > max_speed:
			max_speed = obj.speed

	rel_times = []
	avg_speeds = []
	avg_colors = []

	for i in range(len(dates)):
		rel_times.append(get_time_sec_difference((dates[0], times[0]), (dates[i], times[i])))
		colors.append((speeds[i] / max_speed, green, blue, alpha))
	for i in range(len(dates)-1):
		avg_speeds.append((speeds[i] + speeds[i+1]) / 2.0)
		avg_colors.append((avg_speeds[i] / max_speed, green, blue, alpha))


	# plot the data
	plt.figure()
	plt.scatter(timestamps, rel_times, color = colors)
	plt.title(f'Video: {vid_num} by User: {user_id}', pad=20)
	plt.xlabel('Video Timestamp [sec]')
	plt.ylabel(f'Time [sec] Rel to {dates[0]}, {times[0]}')

	# create the color map and bar
	colordict = {
		'red': [(0, 0, 0, alpha), (1, 1, 1, alpha)],
		'green': [(0, green, green, alpha), (1, green, green, alpha)],
		'blue': [(0, blue, blue, alpha), (1, blue, blue, alpha)]
	}
	colormap = LinearSegmentedColormap('colormap', segmentdata=colordict)
	norm = matplotlib.colors.Normalize(vmin=0, vmax=max_speed)
	plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=matplotlib.cm.cool), label='Video Speed')

	# save the graph as a png
	GRAPH_PATH_REL_STATIC = f'images/{user_id}_{vid_num}.png'
	SAVE_GRAPH_DIR = os.path.join(STATIC_DIR, GRAPH_PATH_REL_STATIC)
	plt.savefig(SAVE_GRAPH_DIR)
	return GRAPH_PATH_REL_STATIC


# positive difference means time2 is in the future
# helper function to be used above
def get_time_sec_difference(datetime1, datetime2):
	date1, time1 = datetime1
	date2, time2 = datetime2

	# datetime(year, month, day, hour, minute, second)
	datetimeObj1 = datetime.datetime(int(date1[:4]), int(date1[5:7]), int(date1[8:10]), int(time1[:2]), int(time1[3:5]), int(time1[6:8]))
	datetimeObj2 = datetime.datetime(int(date2[:4]), int(date2[5:7]), int(date2[8:10]), int(time2[:2]), int(time2[3:5]), int(time2[6:8]))
	difference = datetimeObj2 - datetimeObj1
	return difference.total_seconds()
