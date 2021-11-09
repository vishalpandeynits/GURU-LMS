from django import forms
from .models import Classroom

class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name','need_permission','description','classroom_pic']