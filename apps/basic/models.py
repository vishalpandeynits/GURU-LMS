from django.db import models
from django.contrib.auth.models import User

class Bug_report(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	bug = models.CharField(max_length = 100)
	description = models.TextField()
	approved = models.BooleanField(default=False)
	screenshot = models.ImageField(upload_to="bugs/",null=True,blank=True)
	reported_at = models.DateTimeField(auto_now_add=True)