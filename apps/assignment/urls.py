from django.urls import path
from . import views
 
urlpatterns = [
    path('<unique_id>/<subject_id>/',views.assignments_list,name="assignments"),
    path('<unique_id>/<subject_id>/<id>/',views.assignment_details,name="assignment_page"),
    path('<unique_id>/<subject_id>/<id>/handle/',views.assignment_handle,name="assignment-handle"),
    path('<unique_id>/<subject_id>/<id>/delete/',views.assignment_delete,name="delete_assignment"),
    path('<unique_id>/<subject_id>/<id>/export-marks',views.export_marks,name="export_marks"),
]