from django import forms
from .models import Poll, Choice
from django.conf import settings

class QuestionForm(forms.ModelForm):
	announce_at = forms.DateTimeField(input_formats = settings.DATETIME_INPUT_FORMATS)
	class Meta:
		model = Poll
		fields = ['topic','poll_details','who_can_vote',]

	field_order = ['topic', 'who_can_vote', 'announce_at','poll_details']

class PollUpdateForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['topic','poll_details','announce_at']

	field_order = ['topic', 'announce_at','poll_details']

class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']