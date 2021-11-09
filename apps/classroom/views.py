from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from .forms import CreateclassForm
from .models import Classroom
from apps.subject.models import Subject
from apps.utils import unique_id, members_only
from django.urls import reverse
from notifications.signals import notify
    
@login_required
def homepage(request):
    """
    Create a classroom and joins a classroom.
    """
    user = request.user
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        
        try:
            classroom = get_object_or_404(Classroom, unique_id=join_key)
        except Classroom.DoesNotExist:
            messages.add_message(request, messages.WARNING,"No such classroom exists.")
            return redirect(reverse('homepage'))

        if classroom.members.filter(username=user.username).exists():
            messages.add_message(request, messages.INFO,"You are already member of this class.")
            return redirect(reverse('homepage'))

        if classroom.need_permission:
            classroom.pending_members.add(user)
            messages.add_message(request, messages.SUCCESS,"Your request is sent.\
             You can access classroom material when someone lets you in.")
            user.profile.pending_invitations.add(classroom)
            notify.send(sender=user,verb=f"{user.username} wants to join {classroom.class_name}",recipient=classroom.special_permissions.all(),
            url=reverse('classroom_page',kwargs={
                'unique_id':classroom.unique_id
            }
            ))
        else:
            recipients = User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
            url = reverse('profile',kwargs={'username':user.username})
            notify.send(sender=user,recipient=recipients,verb=f"{request.user.username} has joined {classroom.class_name}",url= url)
            classroom.members.add(user)
        return redirect(reverse('homepage'))

    #create classroom
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST ,request.FILES)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.unique_id = unique_id()
            classroom.created_by = request.user
            classroom.save()
            classroom.members.add(request.user)
            classroom.special_permissions.add(request.user)
            return redirect(reverse('homepage'))
    else:
        createclassform = CreateclassForm()
    params={
        'createclassform':createclassform,
        }
    return render(request,'homepage.html',params)

@login_required
def admin_status(request,unique_id,username):
    """
    Toggles admin status of users from a classroom
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin = classroom.special_permissions.filter(username=request.user.username).exists()
    if admin:
        check = classroom.special_permissions.filter(username = username).exists()
        user = get_object_or_404(User,username=username)
        url = reverse('classroom_page',kwargs={ 'unique_id':unique_id})
        if check:
            if classroom.created_by == user:
                messages.add_message(request,messages.WARNING,"This user have created\
                 this class. He can't be dropped")
                return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))
            classroom.special_permissions.remove(user)
            notify.send(sender=request.user,recipient = user,verb=f"You are no longer admin of {classroom.class_name}",url=url)
        else:
            classroom.special_permissions.add(user)
            notify.send(sender=request.user,recipient = user,verb=f"Now you are admin of {classroom.class_name}",url=url)

        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id})) 
    else:
        raise Http404()

@members_only
def classroom_page(request,unique_id):
    """
    Classroom Setting Page.
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    pending_members = classroom.pending_members.all()
    admins = classroom.special_permissions.all()
    members =  admins | classroom.members.all()
    is_admin = classroom.special_permissions.filter(username = request.user.username).exists()
    #classroom_update
    if request.method=="POST":
        form = CreateclassForm(request.POST,request.FILES,instance=classroom)
        if form.is_valid():
            form.save()
            return redirect(reverse('subjects',kwargs={'unique_id':classroom.unique_id}))
    else:
        form = CreateclassForm(instance=classroom)
    params={
        'members':members.distinct(),
        'admins':admins,
        'pending_members':pending_members,
        'classroom':classroom,
        'is_admin':is_admin,
        'form':form,
    }
    return render(request,'classroom_settings.html',params)

@login_required
def remove_member(request,unique_id,username):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    remove_this_user = get_object_or_404(User,username=username)
    url = reverse('classroom_page',kwargs={'unique_id':classroom.unique_id})
    if admin_check or request.user==remove_this_user:
        if remove_this_user == classroom.created_by:
            messages.add_message(request,messages.WARNING,"This user can't be dropped. He has created this classroom.")
            return redirect(url)
        classroom.members.remove(remove_this_user)
        classroom.teacher.remove(remove_this_user)
        classroom.special_permissions.remove(remove_this_user)
        verb = f"You are removed/left from {classroom.class_name}"
        notify.send(sender=request.user,verb=verb,recipient=remove_this_user,url='#')
        if request.user==remove_this_user:
            return redirect(reverse('homepage'))
        else:
            return redirect(url)
    else:
        raise Http404()

@login_required
def accept_request(request,unique_id,username):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        user = get_object_or_404(User,username=username)
        classroom.members.add(user)
        classroom.pending_members.remove(user)
        user.profile.pending_invitations.remove(classroom)
        url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
        verb = f'Yor request to join classroom {classroom.class_name} is accepted'
        notify.send(sender=request.user,verb=verb,recipient=user,url=url)
        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))

@login_required
def delete_request(request,unique_id,username):
    """ If you don't want to accept the request """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        user = User.objects.get(username=username)
        classroom.pending_members.remove(user)
        verb = "Your request to join class {classroom.class_name} is rejected"
        url = "#"
        notify.send(sender=request.user,verb=verb,recipient=user,url=url)
        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))

@login_required
def unsend_request(request,unique_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if classroom in request.user.profile.pending_invitations.all():
        request.user.profile.pending_invitations.remove(classroom)
        classroom.pending_members.remove(request.user)
        return redirect(reverse('profile',kwargs={
            'username':request.user.username
        }))
    else:
        raise Http404()