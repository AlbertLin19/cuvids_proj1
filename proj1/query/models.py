from django.db import models

# will store the number of queries made of each attribute
class UserCount(models.Model):
	user_id = models.IntegerField()
	count = models.IntegerField()
	def __str__(self):
		return self.user_id

class VideoCount(models.Model):
	vid_num = models.IntegerField()
	count = models.IntegerField()
	def __str__(self):
		return self.vid_num

class WatchData(models.Model):
	date = models.CharField(max_length=10)
	time = models.CharField(max_length=25)
	speed = models.FloatField()
	vid_timestamp = models.FloatField()
	user_id = models.IntegerField()
	vid_num = models.IntegerField()

