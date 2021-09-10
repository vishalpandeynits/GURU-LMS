from .models import Classroom
from django.conf import settings
def data(request,params={}):
    user = request.user
    if user.is_authenticated:
        my_classes = Classroom.objects.all().filter(members=user).reverse()
        read = user.notifications.read()
        params ={
            'classes':my_classes,
            'read':read
        }
    params['x']= request.scheme+ request.META['HTTP_HOST'] + '/'
    return params