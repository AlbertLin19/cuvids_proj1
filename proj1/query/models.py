from django.db import models

# will store the number of queries made of each attribute
class UserCount(models.Model):
	user_id = models.CharField(max_length=20)
	count = models.IntegerField()
	def __str__(self):
		return self.user_id

class VideoCount(models.Model):
	vid_num = models.CharField(max_length=4)
	count = models.IntegerField()
	def __str__(self):
		return self.vid_num