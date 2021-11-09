from django.contrib import admin
from .models import Subject, Subject_activity

class SubjectAdmin(admin.ModelAdmin):
	list_display = ['subject_name','classroom','teacher',] 
	list_display_links = ['subject_name','classroom','teacher',] 
	list_filter = ['subject_name','classroom','teacher',] 
	search_fields = ['subject_name','classroom','teacher',]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Subject_activity)