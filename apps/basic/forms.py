from django import forms
from .models import Bug_report

class BugReportForm(forms.ModelForm):
	screenshot = forms.ImageField(label='Screenshot(optional)',required=False)
	class Meta:
		model = Bug_report
		fields = ['bug','description']