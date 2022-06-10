from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from apps.subject.models import Subject

from notifications.signals import notify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from apps.subject.models import Subject_activity

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to="notes",null=True,blank=True,)
	topic = models.CharField(max_length=100,)
	description = QuillField(null=True,blank=True)
	uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.topic

@receiver(post_save, sender=Note)
def note_signal(sender, instance, created, **kwargs):
	if created:
		students = instance.subject_name.classroom.members.all().difference(
			instance.subject_name.classroom.teacher.all(), 
			instance.subject_name.classroom.special_permissions.all()
			)
		activity = Subject_activity(subject=instance.subject_name,actor=instance.uploaded_by)
		activity.action = "A new note is added."
		activity.url = reverse('read_note', kwargs={
			'unique_id':instance.subject_name.classroom.unique_id,
			'subject_id':instance.subject_name.id,
			'id':instance.id
			})
		activity.save()
		notify.send(sender=instance.uploaded_by,recipient=students,verb=activity.action,url= activity.url)
		from apps.email import note_email
		note_email(instance.id)
		print(1)