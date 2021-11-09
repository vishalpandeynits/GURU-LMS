from apps.email import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Bug_report
from .forms import BugReportForm

@csrf_exempt
def home(request): 
    """Landing Page"""
    if request.user.is_authenticated:
        return redirect(reverse('homepage'))
    if request.method=='POST': # celery email
        name = request.POST.get('name')
        email = request.POST.get('email')
        message =f"{name} \n {email} \n {request.POST.get('message')} "
        mail_subject = 'Contact us : Sent by ' + name 
        if(send_mail(mail_subject,message,'guru.online.classroom.portal@gmail.com',['guru.online.classroom.portal@gmail.com'])):
            messages.add_message(request,messages.SUCCESS,'Your message sent successfully.')
        else:
            messages.add_message(request,messages.ERROR,"An Error while sending your message.\
                Please try again or contact using given contact details.")
    return render(request,'intro.html')

def features(request):
    return render(request, 'features.html')

def privacy(request):
    return render(request, 'privacy.html')

@login_required
def bug_report(request):
    reporters = cache.get('reporters')
    if not reporters:
        reporters = (User.objects.filter(
            id__in=Bug_report.objects.values_list('user__id',flat=True)
            )
            .annotate(itemcount=Count('bug_report')).order_by('-itemcount')[:20]
        )
        cache.set('reporters', reporters, 15*60)
        
    if request.method=="POST":
        form = BugReportForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = BugReportForm()
    params={
        'form':form,
        'reporters':reporters
    }
    return render(request,'bug_report.html',params)