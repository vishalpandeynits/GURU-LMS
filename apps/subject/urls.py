from django.urls import path,include
from .views import *

urlpatterns = [
    path('<unique_id>/',subjects,name="subjects"),
    path('<unique_id>/<subject_id>/subject_details/',subject_details,name="subject_details"),
    path('<unique_id>/<int:subject_id>/delete/',delete_subject,name="delete_subject"), 
    path('<unique_id>/<subject_id>/upload_permissions/<username>/',manage_upload_permission,name="upload_permissions"),
]