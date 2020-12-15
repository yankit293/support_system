from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from .form import RequestForm, ReportUserForm, ReportContentForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from .models import RaiseRequest, ReportUser, ReportContent
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request, 'support.html')

def blog(request):
    return render(request, 'blog.html')

def embed(request):
    return render(request, 'embed.html')

@login_required(login_url='/user/login')    
def paymentissue(request):
    if request.method == 'POST':
        filled_form = RequestForm(request.POST, request.FILES)
        if filled_form.is_valid():
            saving=filled_form.save(commit=False)
            saving.user = request.user
            saving.save()
            '''name = filled_form.cleaned_data['name']
            sender = filled_form.cleaned_data['email']
            issue = filled_form.cleaned_data['issue']
            subject = "{}:{} request at Piblitz".format(name,issue)
            html_message = render_to_string('email-inlined.html',{'name':name})
            plain_message = strip_tags(html_message)
            recipient = []
            recipient.append(sender)
            send_mail(subject,plain_message,from_email=None, recipient_list=recipient,html_message=html_message,fail_silently=False,)'''
            note = 'Thanks for sending request!'
            email = filled_form.cleaned_data['email']
            issue = filled_form.cleaned_data['issue']
            user = request.user
            status_data_pt = RaiseRequest.objects.get(email = email, issue= issue, user=user)
            id = status_data_pt.id
            messages.success(request, "Your Request is submitted Successfully. Wait for Our Confirmation mail.")
            return HttpResponseRedirect('status/'+ str(id))
        else:
            email = filled_form.cleaned_data['email']
            issue = filled_form.cleaned_data['issue']
            user = request.user
            if RaiseRequest.objects.filter(email = email, issue= issue, user=user).exists(): 
                status_data_pt = RaiseRequest.objects.get(email = email, issue= issue, user=user)
                id = status_data_pt.id
                messages.warning(request, "This request is already submitted.")
                return HttpResponseRedirect('status/'+ str(id))
            return render(request, 'payment-issue.html', {'requestform': filled_form})     

        return render(request, 'payment-issue.html', {'requestform': filled_form, 'note': note})
    else:
        form = RequestForm()
        return render(request, 'payment-issue.html', {'requestform': form})

@login_required(login_url='/user/login')
def paymentallissuestatus(request):
    user = request.user
    status_all_data = RaiseRequest.objects.filter(user=user)
    return render(request, 'status.html', {'status':status_all_data})

@login_required(login_url='/user/login')
def paymentissuestatus(request, id):
    link = id
    user = request.user
    status_data = RaiseRequest.objects.get(id=link, user=user)
    return render(request, 'status.html', {'statusdata':status_data})

@login_required(login_url='/user/login')
def deletepaymentissue(request, pk=None):
    if request.method == "POST":
        obj = RaiseRequest.objects.get(id=pk)
        obj.delete()
        return redirect('/support/paymentissue/status/')

#Report User 
@login_required(login_url='/user/login')
def reportuser(request):
    if request.method == 'POST':
        filled_form = ReportUserForm(request.POST, request.FILES)
        if filled_form.is_valid():
            saving=filled_form.save(commit=False)
            saving.user = request.user
            saving.save()
            email = filled_form.cleaned_data['email']
            username = filled_form.cleaned_data['username']
            reason = filled_form.cleaned_data['reason']
            user = request.user 
            report_status = ReportUser.objects.get(email = email, username = username, reason = reason, user=user)
            id = report_status.id
            messages.success(request, "Your Request is submitted Successfully. Wait for Our Confirmation mail.")
            return HttpResponseRedirect('status/'+ str(id))
        else:
            email = filled_form.cleaned_data['email']
            username = filled_form.cleaned_data['username']
            reason = filled_form.cleaned_data['reason']
            user = request.user
            if ReportUser.objects.filter(email = email, username = username, reason = reason, user=user).exists(): 
                report_status = ReportUser.objects.get(email = email, username = username, reason = reason, user=user)
                id = report_status.id
                messages.warning(request, "This report is already submitted.")
                return HttpResponseRedirect('status/'+ str(id))
        return render(request, 'report-user.html', {'reportuserform': filled_form}) 
    else:
        form = ReportUserForm()
        return render(request, 'report-user.html', {'reportuserform': form})

def get_usernames(request): 
    if request.is_ajax():
        current_user = request.user
        q = request.GET.get('username')
        if q:
            usernames = User.objects.filter(username__startswith=q).exclude(username=current_user)
            results = []
            for un in usernames:
                key = ['username','name', 'email']
                value = [un.username, str(un.first_name + ' ' + un.last_name), un.email]
                user = dict(zip(key, value))
                results.append(user)
        else:
            results = None
        return JsonResponse(results, safe=False)
    return render(request, 'report-user.html')

@login_required(login_url='/user/login')
def reportalluserstatus(request):
    user = request.user
    reportuser_alldata = ReportUser.objects.filter(user=user)
    return render(request, 'reportuser-status.html', {'reportuserdata':reportuser_alldata})

@login_required(login_url='/user/login')
def reportuserstatus(request, id):
    link = id
    user = request.user
    reportuser_data = ReportUser.objects.get(id=link, user=user)
    return render(request, 'reportuser-status.html',{'reportuserstatus':reportuser_data})


def delete_report_user(request, pk):
    if request.method == "POST":
        obj = ReportUser.objects.get(id=pk)
        obj.delete()
        return redirect('/support/reportuser/status/')

#Report Content
@login_required(login_url='/user/login')
def reportcontent(request):
    if request.method == 'POST':
        filled_form = ReportContentForm(request.POST, request.FILES)
        if filled_form.is_valid():
            saving=filled_form.save(commit=False)
            saving.user = request.user
            saving.save()
            filled_form = ReportContentForm()
            note = 'Thanks for sending request!'
            return render(request, 'reportcontent-status.html', {'note':note})
        else:
            email = filled_form.cleaned_data['email']
            subject = filled_form.cleaned_data['subject']
            reason = filled_form.cleaned_data['reason']
            user = request.user
            if ReportContent.objects.filter(email = email, subject = subject, reason = reason, user=user).exists(): 
                report_status = ReportContent.objects.get(email = email, subject = subject, reason = reason, user=user)
                id = report_status.id
                messages.warning(request, "This report is already submitted.")
                return HttpResponseRedirect('status/'+ str(id))
        return render(request, 'report-content.html', {'reportcontentform': filled_form}) 
    else:
        form = ReportContentForm()
        return render(request, 'report-content.html', {'reportcontentform': form})

@login_required(login_url='/user/login')
def reportallcontentstatus(request):
    user = request.user
    reportcontent_alldata = ReportContent.objects.filter(user=user)
    return render(request, 'reportcontent-status.html', {'reportcontentdata':reportcontent_alldata})

def reportcontentstatus(request, id):
    link = id
    user = request.user
    reportcontent_data = ReportContent.objects.get(id=link, user=user)
    return render(request, 'reportcontent-status.html',{'reportcontentstatus':reportcontent_data})


def delete_report_content(request, pk):
    if request.method == "POST":
        obj = ReportContent.objects.get(id=pk)
        obj.delete()
        return redirect('/support/reportcontent/status/')