from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from apps.subject.models import Subject

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to="notes",null=True,blank=True,)
	topic = models.CharField(max_length=100,)
	description = QuillField(null=True,blank=True)
	uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.topic