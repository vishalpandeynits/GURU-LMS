from django.contrib import admin
from .models import Assignment, Submission

class AssignmentAdmin(admin.ModelAdmin):
	list_display = ['subject_name','topic','submission_date','assigned_by','full_marks']
	search_fields = ['subject_name','topic','submission_date','assigned_by','description']

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ['assignment','submitted_by','submitted_on']
	search_fields = ['assignment','submitted_by','submitted_on']

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission,SubmissionAdmin)