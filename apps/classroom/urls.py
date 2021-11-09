from django.urls import path
from . import views

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('<unique_id>/',views.classroom_page,name="classroom_page"),
    path('<unique_id>/<username>/Classadmin/',views.admin_status,name="class_admin"),
    path('<unique_id>/<str:username>/remove/',views.remove_member, name="remove_member"),
    path('<unique_id>/<str:username>/accept/',views.accept_request, name="accept_request"),
    path('<unique_id>/<str:username>/delete/',views.delete_request, name="delete_request"),
    path('<unique_id>/unsend-request',views.unsend_request,name="unsend_request"),
]