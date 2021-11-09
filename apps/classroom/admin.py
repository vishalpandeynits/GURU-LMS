from django.contrib import admin
from .models import Classroom

class ClassroomAdmin(admin.ModelAdmin):
	list_display = ['class_name','unique_id','created_by',] 
	date_hierarchy = 'created_on'
	list_display_links = ['class_name','unique_id']
	list_filter = ['class_name','created_by',]
	search_fields = ['class_name','unique_id']

# Register your models here.
admin.site.register(Classroom,ClassroomAdmin)
