from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserCount, VideoCount, WatchData
import fetch

# home page: search for users
def userQuery(request):

	context = {
		'users': fetch.get_users()
	}
	return render(request, 'query/user_query.html', context)

# video search page: reached after user ID is selected
def vidQuery(request):
	user_id = request.GET.get('user_id')
	# check that the user_id is a number
	if not user_id.isdigit():
		messages.warning(request, f"Invalid user ID given - redirecting back to user ID search!")
		return redirect('user-query')
	vid_nums = fetch.get_vids_for_user(user_id)
	context = {
		"vid_nums": vid_nums,
		"user_id": user_id
	}

	# check that the user_id exists
	if not vid_nums:
		messages.warning(request, f"Invalid user ID given - redirecting back to user ID search!")
		return redirect('user-query')

	# ask for a video number
	messages.success(request, f"Showing videos watched by '{user_id}'!")
	return render(request, 'query/video_query.html', context)

# output from the user ID and video number query
def response(request):
	user_id = request.GET.get('user_id')
	vid_num = request.GET.get('vid_num')
	# check that the vid_num is a number
	if not vid_num.isdigit():
		messages.warning(request, f"Invalid video number given - redirecting back to user ID search!")
		return redirect('user-query')

	# check that the vid_num exists for that user
	plot = fetch.get_watch_patten_graph(user_id, vid_num)
	context = {'plot': plot}
	if not plot:
		messages.warning(request, f"Invalid video number given - redirecting back to user ID search!")
		return redirect('user-query')

	# update the user and video query counts
	user = UserCount.objects.filter(user_id=user_id)
	video = VideoCount.objects.filter(vid_num=vid_num)
	if user:
		user.update(count = user.first().count + 1)
	else:
		UserCount.objects.create(user_id=user_id, count=1)
	if video:
		video.update(count = video.first().count + 1)
	else:
		VideoCount.objects.create(vid_num=vid_num, count=1)

	# display the graph
	return render(request, 'query/response.html', context)

# display stored query counts
def queryCounts(request):
	context = {
		'user_counts': UserCount.objects.all(),
		'video_counts': VideoCount.objects.all()
	}
	return render(request, 'query/query_counts.html', context)

# reset all the query counts
def reset(request):
	UserCount.objects.all().delete()
	VideoCount.objects.all().delete()
	messages.success(request, f'All query counts reset!')
	return redirect('user-query')