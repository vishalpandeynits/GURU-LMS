from django import forms
from django.conf import settings
from .models import Assignment, Submission
from django.forms.widgets import NumberInput

class AssignmentForm(forms.ModelForm):
	submission_date = forms.DateTimeField(input_formats = settings.DATETIME_INPUT_FORMATS)
	class Meta:
		model = Assignment
		fields = ['topic','full_marks','file','description']
		widgets = {
				'full_marks':NumberInput(attrs={'max-value': '100'})
			}
	field_order = ['topic', 'submission_date', 'full_marks','description']

class SubmitAssignmentForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['file']