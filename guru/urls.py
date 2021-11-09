from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import views
from apps.users.forms import UserLoginForm
import notifications.urls
from decouple import config

urlpatterns = [
    path('AKIAUMKLYNQMHJ3N2H7Q/', admin.site.urls),
    path('', include('apps.basic.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('polls/',include('apps.poll.urls')),
    path('profile/',include('apps.users.urls')),
    path('comments/', include('django_comments.urls')),
    path('accounts/', include('allauth.urls')),
    path('rest/',include('rest_framework.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('accounts/password_reset/', views.PasswordResetView.as_view(
    html_email_template_name='registration/password_reset_html_email.html',
    extra_email_context={ 'SITE_NAME':settings.SITE_NAME }
    )),
    path('accounts/login/',views.LoginView.as_view(template_name="registration/login.html",
        authentication_form=UserLoginForm),name='login'
    ),
]
if config('DEBUG') == 'DEVELOPMENT':
    urlpatterns += [path('admin/', admin.site.urls)]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)