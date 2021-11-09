from django.db import models
from django.contrib.auth.models import User
# from imagekit.models import ProcessedImageField
# from guru.storage_back import PrivateMediaStorage
# from imagekit.processors import ResizeToFill

class Classroom(models.Model):
	created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='created_by')
	members = models.ManyToManyField(User)
	teacher = models.ManyToManyField(User, related_name='classroom_teachers')
	special_permissions = models.ManyToManyField(User, related_name= "special_permissions")
	pending_members = models.ManyToManyField(User,related_name='pending_members')
	# classroom_pic = ProcessedImageField(upload_to="classroom",default="classroom.jpg",storage=PrivateMediaStorage(),null=True,
	# processors=[ResizeToFill(1000, 1000)],format='JPEG',options={'quality': 100})
	classroom_pic = models.ImageField(upload_to="classroom",default="classroom.jpg", null=True)
	class_name = models.CharField(max_length = 50)
	description = models.TextField(null=True, blank=True,max_length=300)
	created_on = models.DateTimeField(auto_now_add=True)
	unique_id = models.CharField(max_length=16,unique=True)
	need_permission = models.BooleanField(default=True)

	def __str__(self):
		return self.class_name