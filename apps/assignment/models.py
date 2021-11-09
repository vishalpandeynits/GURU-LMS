from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from apps.subject.models import Subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to="assignments",null=True,blank = True,)
	topic = models.CharField(max_length=100,)
	description = QuillField(null=True,blank=True)
	submission_date = models.DateTimeField() 
	assigned_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_by = models.ManyToManyField(User,related_name="Submissions")
	full_marks = models.IntegerField(default=100)
	submission_link = models.BooleanField(default=True)

	def __str__(self):
		return "Assignment on "+ self.topic

class Submission(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(upload_to="submissions",)
	submitted_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_on = models.DateTimeField(auto_now_add=True)
	current_status = models.BooleanField(default=False)
	marks_assigned = models.IntegerField(null=True,blank=True)
	history = models.CharField(max_length=5000,null=True,blank=True)
	def __str__(self):
		return "Assignment upload of "+self.assignment.topic + self.submitted_by.username