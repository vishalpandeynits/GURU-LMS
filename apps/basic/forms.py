from django import forms
from .models import Bug_report, Classroom, Subject, Note, Announcement, Assignment, Submission
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
from django.conf import settings 
class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name','need_permission','description','classroom_pic']
	
class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name']

class SubjectEditForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name','subject_pic','description']

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['topic','file','description']
		

class AssignmentForm(forms.ModelForm):
	submission_date = forms.DateTimeField(input_formats = settings.DATETIME_INPUT_FORMATS)
	class Meta:
		model = Assignment
		fields = ['topic','full_marks','file','description']
		widgets = {
				'full_marks':NumberInput(attrs={'max-value': '100'})
			}
	field_order = ['topic', 'submission_date', 'full_marks','description']

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['subject','file','description']

class SubmitAssignmentForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['file']

class BugReportForm(forms.ModelForm):
	screenshot = forms.ImageField(label='Screenshot(optional)',required=False)
	class Meta:
		model = Bug_report
		fields = ['bug','description']
