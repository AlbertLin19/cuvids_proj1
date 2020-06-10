from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserCount, VideoCount

def userQuery(request):
	return render(request, 'query/user_query.html')

def vidQuery(request):
	user_id = request.GET.get('user_id')
	context = {"user_id": user_id}

	# check that the user_id exists
	if not True:
		messages.error(request, f"Invalid User ID given - redirecting back to User ID search!")
		return redirect('user-query')

	# ask for a video number
	messages.success(request, f"Showing videos watched by '{user_id}'!")
	return render(request, 'query/video_query.html', context)

def response(request):
	user_id = request.GET.get('user_id')
	vid_num = request.GET.get('vid_num')
	context = { '' : None}

	# check that the vid_num exists for that user
	if not True:
		messages.error(request, f"Invalid Video Number given - redirecting back to User ID search!")
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
	return render(request, 'query/response.html', context)

def queryCounts(request):
	context = {
		'user_counts': UserCount.objects.all(),
		'video_counts': VideoCount.objects.all()
	}
	return render(request, 'query/query_counts.html', context)

def reset(request):
	UserCount.objects.all().delete()
	VideoCount.objects.all().delete()
	messages.success(request, f'All Query Counts reset!')
	return redirect('user-query')