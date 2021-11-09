from django import forms
from .models import Subject
	
class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name']

class SubjectEditForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name','subject_pic','description']