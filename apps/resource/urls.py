from django.urls import path,include
from .views import *

urlpatterns = [
    path('<unique_id>/<subject_id>/',notes_list,name="resources"),
    path('<unique_id>/<subject_id>/<id>/read/',note_details,name="read_note"),
    path('<unique_id>/<subject_id>/<id>/delete/',note_delete,name="delete_resource"),
]