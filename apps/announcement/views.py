from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.db.models import Q
from .forms import AnnouncementForm
from .models import Announcement
from apps.utils import members_only, pagination, extension_type
from apps.delete_notify import announcement_delete_notify
from django.urls import reverse
from apps.classroom.models import Classroom
from apps.subject.models import Subject

@members_only
@login_required#checked
def announcements_list(request, unique_id, subject_id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    #querysets
    subject = get_object_or_404(Subject,id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    announcements = Announcement.objects.all().filter(subject_name=subject)
    if request.GET.get('search'):
        search = request.GET.get('search')
        announcements = announcements.filter(Q(subject__icontains=search)|Q(description__icontains=search))
    query,page_range = pagination(request,announcements)
    announcements=query.object_list

    #announcement form handling
    if is_teacher:
        if request.method=="POST":
            form = AnnouncementForm(request.POST,request.FILES)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.subject_name = subject
                announcement.announced_by = request.user
                announcement.save()
                return redirect(reverse('announcement',kwargs=
                    {'unique_id':classroom.unique_id,'subject_id':subject.id}))
        else:
            form= AnnouncementForm()
    params={
            'form':form,
            'subject':subject,
            'classroom':classroom,
            'announcements':announcements,
            'page':query,
            'page_range':page_range,
            'is_teacher':is_teacher
        }
    return render(request,'announcements/announcement_list.html',params)

@members_only
@login_required#checked
def announcement_details(request,unique_id,subject_id,id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    announcement = get_object_or_404(Announcement,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher

    #announcement update handling
    if is_teacher:
        if request.method=="POST":
            form = AnnouncementForm(request.POST,request.FILES,instance=announcement)
            if form.is_valid():
                announcementform = form.save(commit=False)
                announcementform.subject_name = subject
                announcementform.save()
                return redirect(reverse('announcement_page',kwargs={
                    'unique_id':classroom.unique_id,
                    'subject_id':subject.id,
                    'id':announcement.id
                    }))
        else:
            form= AnnouncementForm(instance=announcement)
    params={
        'announcement':announcement,
        'extension':extension_type(announcement.file),
        'subject':subject,
        'updateform':form,
        'classroom':classroom,
        'is_teacher':is_teacher,
        }
    return render(request,'announcements/announcement_details.html',params)

@login_required
def announcement_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    announcement = get_object_or_404(Announcement,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    #notify
    if is_teacher:
        announcement.delete()
        announcement_delete_notify(request,announcement)
        return redirect(reverse('announcement',kwargs={
            'unique_id':classroom.unique_id,
            'subject_id':subject.id
            }))
    else:
        raise Http404()