from .models import Announcement
from django.forms import ModelForm

class AnnouncementForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ['subject','file','description']