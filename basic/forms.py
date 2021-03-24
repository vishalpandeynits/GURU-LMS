from django import forms
from .models import Bug_report, Classroom, Subject, Note, Announcement, Assignment, Submission
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError

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
		
	def clean(self,*args, **kwargs):
		if 'description' not in self.cleaned_data.keys():
			print("nhi hai")
			raise ValidationError('Description must not be less than 20 characters.')
		return self.cleaned_data

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['topic','full_marks','submission_date','file','description']
		widgets = {
				'full_marks':NumberInput(attrs={'max-value': '100'})
			}

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
