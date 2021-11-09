from django.urls import path
from .import views

urlpatterns = [
    path('announcement/<unique_id>/<subject_id>/',views.announcements_list,name="announcement"),
    path('announcement/<unique_id>/<subject_id>/<id>/',views.announcement_details,name="announcement_page"),
    path('announcement/<unique_id>/<subject_id>/<id>/delete/',views.announcement_delete,name="delete_announcement"),
]