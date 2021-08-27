from django.contrib import admin
from .models import *

class ClassroomAdmin(admin.ModelAdmin):
	list_display = ['class_name','unique_id','created_by',] 
	date_hierarchy = 'created_on'
	list_display_links = ['class_name','unique_id']
	list_filter = ['class_name','created_by',]
	search_fields = ['class_name','unique_id']

class SubjectAdmin(admin.ModelAdmin):
	list_display = ['subject_name','classroom','teacher',] 
	list_display_links = ['subject_name','classroom','teacher',] 
	list_filter = ['subject_name','classroom','teacher',] 
	search_fields = ['subject_name','classroom','teacher',]

class NoteAdmin(admin.ModelAdmin):
	list_display = ['topic','uploaded_by','subject_name','uploaded_on']
	search_fields = ['topic','uploaded_by','subject_name','uploaded_on']

class AssignmentAdmin(admin.ModelAdmin):
	list_display = ['subject_name','topic','submission_date','assigned_by','full_marks']
	search_fields = ['subject_name','topic','submission_date','assigned_by','description']

class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ['subject_name','subject','announced_by']
	fields = (('url', 'subject_name'), 'subject')
	search_fields = ['subject_name','subject','announced_by','description']

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ['assignment','submitted_by','submitted_on']
	search_fields = ['assignment','submitted_by','submitted_on']

class BugReportAdmin(admin.ModelAdmin):
	list_display = ['bug','user','reported_at']
	search_fields = ['bug','user','description']

# Register your models here.
admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Announcement,AnnouncementAdmin)
admin.site.register(Submission,SubmissionAdmin)
admin.site.register(Subject_activity)
admin.site.register(Bug_report,BugReportAdmin)
