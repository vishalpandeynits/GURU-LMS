from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import views
from apps.users.forms import UserLoginForm
import notifications.urls
from decouple import config

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.basic.urls')),
    path('polls/',include('apps.poll.urls')),
    path('profile/',include('apps.users.urls')),
    path('assignment/', include('apps.assignment.urls')),
    path('announcement/', include('apps.announcement.urls')),
    path('resources/', include('apps.resource.urls')),
    path('classroom/', include('apps.classroom.urls')),
    path('subject/', include('apps.subject.urls')),

    path('accounts/',include('django.contrib.auth.urls')),
    path('rest/',include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    path('comments/', include('django_comments.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('accounts/password_reset/', views.PasswordResetView.as_view(
    html_email_template_name='registration/password_reset_html_email.html',
    extra_email_context={ 'SITE_NAME':settings.SITE_NAME }
    )),
    path('accounts/login/',views.LoginView.as_view(template_name="registration/login.html",
        authentication_form=UserLoginForm),name='login'
    ),  
]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)