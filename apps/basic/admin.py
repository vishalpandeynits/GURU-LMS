from django.contrib import admin
from .models import Bug_report

class BugReportAdmin(admin.ModelAdmin):
	list_display = ['bug','user','reported_at']
	search_fields = ['bug','user','description']

admin.site.register(Bug_report,BugReportAdmin)
