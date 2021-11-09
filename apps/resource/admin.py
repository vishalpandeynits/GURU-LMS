from django.contrib import admin
from .models import Note

class NoteAdmin(admin.ModelAdmin):
	list_display = ['topic','uploaded_by','subject_name','uploaded_on']
	search_fields = ['topic','uploaded_by','subject_name','uploaded_on']

admin.site.register(Note,NoteAdmin)