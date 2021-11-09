from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from .forms import SubjectForm, SubjectEditForm
from .models import *
from apps.email import *
from apps.delete_notify import *
from apps.utils import members_only, pagination
from django.urls import reverse
from notifications.signals import notify
from apps.classroom.models import Classroom

@members_only
def subjects(request, unique_id,form=None):
    """ 
    Enlists all the subjects of a classroom ,
    subjects can be added by admins
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    #querysets
    members = classroom.members.all()
    subjects = Subject.objects.filter(classroom=classroom)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    # Admins can add a subject and assign a teacher to it
    if admin_check and request.method=="POST":
        form = SubjectForm(request.POST)
        teacher = get_object_or_404(User,username=request.POST.get('teacher'))
        if form.is_valid():
            subject=form.save(commit=False)
            subject.classroom=classroom
            subject.teacher = teacher
            subject.save()
            subject.upload_permission.add(teacher)
            recipients=User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
            url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
            notify.send(sender=request.user,verb=f"subject {subject.subject_name} added in {classroom.class_name}",
            recipient=recipients,url=url)
            messages.add_message(request,messages.INFO,f"A new Subject {subject.subject_name} added")
            classroom.teacher.add(teacher)
            return redirect(url)
        else:
            form = SubjectForm()
    params = {
        'subjects':subjects,
        'form':form,
        'classroom':classroom,
        'is_admin':admin_check,
        'members':members
        }
    return render(request,'subjects_list.html',params)

@members_only
@login_required #checked
def subject_details(request,unique_id, subject_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    upload_permission = subject.upload_permission.all()
    members = classroom.members.all()
    admins = classroom.special_permissions.all()
    teachers = classroom.teacher.all()
    teacher = subject.teacher
    members = list((admins| members.difference(teachers)).distinct())
    if teacher not in members:
        members.append(teacher)

    activities = Subject_activity.objects.filter(subject=subject).reverse()
    query,page_range = pagination(request,activities)
    activities=query.object_list

    if request.method=='POST':
        form = SubjectEditForm(request.POST , request.FILES,instance=subject)
        if form.is_valid():
            form.save()
    else:
        form = SubjectEditForm(instance=subject)
    params={
        'subject':subject,
        'classroom':classroom, 
        'is_teacher':admin_check,
        'members':members,
        'upload_permissions':upload_permission,
        'admins':admins,
        'teacher':teacher,
        'page':query,
        'page_range':page_range,
        'form':form
        }
    return render(request,'subject_details.html',params)

@login_required #checked
def delete_subject(request,unique_id, subject_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        verb = "A Subject "+subject.subject_name + " is deleted by "+ request.user.username
        url =reverse('subjects',kwargs={'unique_id':classroom.unique_id})
        recipient = User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
        notify.send(sender=request.user,verb=verb,recipient=recipient,url=url)
        subject.delete()
        return redirect(url)
    else:
        raise Http404()

@members_only
@login_required #checked
def manage_upload_permission(request,unique_id,subject_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)  
    user = User.objects.get(username=username)
    subject = get_object_or_404(Subject,id=subject_id)
    check = subject.upload_permission.filter(username = user.username).exists()
    url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
    if check:
        verb = f"You can't upload notes in {subject.subject_name} of {classroom.class_name} anymore"
        notify.send(sender=request.user,verb=verb,recipient=user,url = url)
        subject.upload_permission.remove(user)
    else:
        verb = f"You got permission to  upload notes in {subject.subject_name} of {classroom.class_name}"
        subject.upload_permission.add(user)
        notify.send(sender=request.user,verb=verb,recipient=user,url = url)
    return redirect(reverse('subject_details',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))