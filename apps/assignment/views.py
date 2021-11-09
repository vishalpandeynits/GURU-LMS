from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.db.models import Q
from .forms import AssignmentForm, SubmitAssignmentForm
from .models import Assignment, Submission
from apps.email import email_marks, send_reminder
from apps.delete_notify import assignment_delete_notify
from apps.utils import members_only, pagination, extension_type
from django.urls import reverse
import xlwt, datetime 
from notifications.signals import notify
from django.core.cache import cache
from apps.classroom.models import Classroom
from apps.subject.models import Subject

@members_only
@login_required#checked
def assignments_list(request ,unique_id, subject_id, form=None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    assignments = Assignment.objects.filter(subject_name=subject)
    search = request.GET.get('search')
    if search:
        assignments = assignments.filter(Q(topic__icontains=search)|Q(description__icontains=search))
    query,page_range = pagination(request,assignments)
    assignments=query.object_list

    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or subject.teacher==request.user

    if is_teacher:
        if request.method=="POST":
            form = AssignmentForm(request.POST,request.FILES)
            datetime_object = datetime.datetime.strptime(request.POST['submission_date'], "%m/%d/%Y %H:%M")
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.submission_date = datetime_object
                assignment.subject_name = subject
                assignment.assigned_by = request.user
                assignment.save()
                return redirect(request.META['HTTP_REFERER'])
        else:
            form= AssignmentForm()

    params={
        'form':form,
        'subject':subject,
        'classroom':classroom,
        'assignments':assignments,
        'page':query,
        'page_range':page_range,
        }
    return render(request,'assignments/assignment_list.html',params)

@members_only
@login_required#checked
def assignment_details(request,unique_id,subject_id,id):
    updateform = form  = submission = submission_object = None
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    assignment = get_object_or_404(Assignment,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    if is_teacher:
        if request.method=="POST":
            updateform = AssignmentForm(request.POST,request.FILES,instance=assignment)
            datetime_object = datetime.datetime.strptime(request.POST['submission_date'], "%m/%d/%Y %H:%M")
            if updateform.is_valid():
                form = updateform.save(commit=False)
                form.submission_date = datetime_object
                form.save()
                return redirect(request.META['HTTP_REFERER'])
        else:
            updateform= AssignmentForm(instance=assignment)
    #submitting assignment
    else: 
        submission_object = Submission.objects.filter(Q(submitted_by=request.user) & Q(assignment=assignment)).first()
        if request.method=="POST":
            if assignment.submission_link:
                form = SubmitAssignmentForm(request.POST, request.FILES,instance=submission_object)
                if(submission_object and submission_object.marks_assigned):
                    messages.add_message(request,messages.WARNING, 'Your assignment is checked, You can\'t change it now')
                    return redirect(request.META['HTTP_REFERER'])
                if form.is_valid():
                    data=form.save(commit=False)
                    data.submitted_by=request.user
                    data.assignment= assignment
                    data.save()
                    assignment.submitted_by.add(request.user)
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.add_message(request,messages.WARNING,"Submission link is closed.")
        else:
            form = SubmitAssignmentForm(instance=submission_object)
    
    params={
        'assignment':assignment,
        'extension':extension_type(assignment.file),
        'subject':subject,
        'form':form,
        'updateform':updateform,
        'classroom':classroom,
        'submissionform':form,
        'submission':submission,
        'submission_object':submission_object,
        'is_teacher':is_teacher,
        }       
    return render(request,'assignments/assignment_detail.html',params)

@login_required#checked
def assignment_handle(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    assignment = get_object_or_404(Assignment,id=id)
    is_teacher = request.user==subject.teacher or request.user == assignment.assigned_by
    
    if is_teacher:
        if request.POST.get('marks_assigned'):
            id  = request.POST.get('id') 
            submission = get_object_or_404(Submission,id=id)
            marks = request.POST.get('marks_assigned')
            submission.marks_assigned = marks
            submission.save()
            url = reverse('assignment_page',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id})
            messages.add_message(request,messages.SUCCESS,'Marks Assigned.')
            notify.send(sender=request.user,verb=f'You got {marks} for your assignment {assignment.topic}',recipient=submission.submitted_by,url =url)
            email_marks(request,submission,assignment)
            return redirect(reverse('assignment-handle',kwargs={
                'unique_id':classroom.unique_id,
                'subject_id':subject.id,
                'id':assignment.id
                }))

    if request.POST.get('toggle_link'):
        assignment.submission_link  = not assignment.submission_link
        assignment.save()

    #list of submissions
    all_submissions = Submission.objects.filter(assignment=assignment)
    late_submissions = all_submissions.filter(submitted_on__gt=assignment.submission_date)
    ontime_submissions = all_submissions.filter(submitted_on__lte=assignment.submission_date)
    members = classroom.members.all()
    teachers = classroom.teacher.all()
    students = members.difference(teachers).difference(classroom.special_permissions.all())
    submitted = assignment.submitted_by.all()
    not_submitted = students.difference(submitted)
    
    if request.POST.get('send_reminder')=='1':
        #send_notification
        recepients = User.objects.filter(username__in=not_submitted.values_list('username', flat=True))
        url = reverse('assignment_page',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id})
        notify.send(sender=request.user,verb=f"Reminder to submit your assignment",recipient=recepients,url=url)
        send_reminder(request,assignment,not_submitted.values_list('email', flat=True))

    params = {
        'assignment':assignment,
        'all_submissions':all_submissions,
        'late_submissions':late_submissions,
        'ontime_submissions':ontime_submissions,
        'is_teacher':is_teacher,
        'submitted':submitted,
        'not_submitted':not_submitted,
        'subject':subject,
        'classroom':classroom,
    }
    return render(request,'assignments/assignment_handle.html',params)

@login_required#checked
def assignment_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    assignment = get_object_or_404(Assignment,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    if is_teacher:
        assignment.delete()
        assignment_delete_notify(request,assignment)
        return redirect(reverse('assignments',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
    else:
        raise Http404()

@login_required#checked
def export_marks(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    subject = get_object_or_404(Subject,id=subject_id)
    if admin_check or request.user==subject.teacher:
        assignment = get_object_or_404(Assignment,id=id)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="mark_sheet of {assignment.topic}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Submissions')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Username','submitted_on','marks_obtained']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        
        rows = Submission.objects.all().filter(assignment=assignment).values_list('submitted_by','submitted_on','marks_assigned')
        rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
        
        for row in rows:
            row_num += 1
            row[0]=str(User.objects.get(id=row[0]))
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
    else:
        raise Http404()