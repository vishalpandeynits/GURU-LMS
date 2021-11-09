from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from apps.delete_notify import note_delete_notify
from apps.utils import members_only, pagination, extension_type
from apps.classroom.models import Classroom
from apps.subject.models import Subject

from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from .forms import NoteForm
from .models import Note

@members_only
@login_required
def notes_list(request,unique_id,subject_id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    #querysets
    subject = get_object_or_404(Subject,id=subject_id)
    notes = Note.objects.filter(subject_name=subject).order_by('-id')
    if request.GET.get('search'):
        search = request.GET.get('search')
        notes = notes.filter(Q(topic__icontains=search)|Q(description__icontains=search)) 
    query,page_range = pagination(request, notes)
    upload_permission = subject.upload_permission.all().filter(username=request.user.username).exists()
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or upload_permission or request.user==subject.teacher  
    #Add note form handling
    if is_teacher:
        if request.method=="POST":
            form = NoteForm(request.POST,request.FILES)
            if form.is_valid:
                data=form.save(commit=False)
                data.subject_name = subject
                data.uploaded_by = request.user
                data.save()
                messages.add_message(request,messages.SUCCESS,f"Your Note {data.topic} is added")
                return redirect(reverse('resources',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
        else:
            form= NoteForm()

    params={
        'form':form,
        'subject':subject,
        'classroom':classroom,
        'notes':notes,
        'page':query,
        'page_range':page_range,
        'is_teacher':is_teacher,
        }
    return render(request,'notes/notes_list.html',params)

@members_only
@login_required
def note_details(request, unique_id, subject_id, id, form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    #queryset
    subject = get_object_or_404(Subject,id=subject_id) 
    note = get_object_or_404(Note,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher or note.uploaded_by == request.user

    if is_teacher:
        if request.method=="POST": 
            form = NoteForm(request.POST,request.FILES,instance=note)
            if form.is_valid():
                form.file = request.POST.get('file')
                form.save()
                return redirect(reverse('read_note',kwargs={
                    'unique_id':classroom.unique_id,
                    'subject_id':subject.id,
                    'id':note.id
                    }))
        else:
            form= NoteForm(instance=note)
    params={
            'subject':subject,
            'updateform':form,
            'note':note,
            'classroom':classroom,
            'is_teacher': is_teacher,
            'extension':extension_type(note.file)
        }
    return render(request,'notes/note_detail.html',params)

@login_required
def note_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    note =  get_object_or_404(Note,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or note.uploaded_by==request.user or request.user==subject.teacher 
    if is_teacher:
        note.delete()
        note_delete_notify(request,note)
        return redirect(reverse('resources',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
    else:
        raise Http404()