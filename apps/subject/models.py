from django.db import models
from django.contrib.auth.models import User
from apps.classroom.models import Classroom

class Subject(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	subject_name = models.CharField(max_length=50)
	teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="teacher")
	upload_permission = models.ManyToManyField(User,related_name="upload_permitted")
	# subject_pic = ProcessedImageField(upload_to="subject_content",default="book.jpg",storage=PrivateMediaStorage(),
	# processors=[ResizeToFill(1000, 1000)],format='JPEG',options={'quality': 100})
	subject_pic = models.ImageField(upload_to="subject_content",default="book.jpg")
	description = models.TextField(null=True,blank=True,max_length=500)

	def __str__(self):
		return self.subject_name

class Subject_activity(models.Model):
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	action = models.CharField(max_length=100)
	actor = models.ForeignKey(User,on_delete = models.CASCADE)
	time = models.DateTimeField(auto_now_add = True)
	url = models.URLField(null=True,blank=True)

	def __str__(self):
		return self.action