from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('features/',features,name="features"),
    path('privacy-policy/',privacy,name="privacy"),
    path('bug-report/',bug_report,name="bug_report"),
]