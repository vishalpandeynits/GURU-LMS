from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ['subject_name','subject','announced_by']
	fields = (('url', 'subject_name'), 'subject')
	search_fields = ['subject_name','subject','announced_by','description']

admin.site.register(Announcement,AnnouncementAdmin)
