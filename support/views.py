from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import HttpResponse
from .form import RequestForm, ReportForm, StatusForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from .models import RaiseRequest
from django.contrib import messages


def index(request):
    return render(request, 'support.html')

def payment(request):
    if request.method == 'POST':
        filled_form = RequestForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            name = filled_form.cleaned_data['name']
            sender = filled_form.cleaned_data['email']
            issue = filled_form.cleaned_data['issue']
            subject = "{}:{} request at Piblitz".format(name,issue)
            html_message = render_to_string('email-inlined.html',{'name':name})
            plain_message = strip_tags(html_message)
            recipient = []
            recipient.append(sender)
            send_mail(subject,plain_message,from_email=None, recipient_list=recipient,html_message=html_message,fail_silently=False,)
            note = 'Thanks for sending request!'
            filled_form = RequestForm()
            return render(request, 'status.html', {'note':note})
        else:
            if RaiseRequest.objects.filter(email = filled_form.cleaned_data['email'], issue= filled_form.cleaned_data['issue']).exists(): 
                status_data_pt = RaiseRequest.objects.get(email = filled_form.cleaned_data['email'], issue= filled_form.cleaned_data['issue'])
                id = status_data_pt.id
                messages.warning(request, "This request is already submitted.")
                return HttpResponseRedirect('/support/status/'+ str(id))
            return render(request, 'payment-issue.html', {'requestform': filled_form})     

        return render(request, 'payment-issue.html', {'requestform': filled_form, 'note': note})
    else:
        form = RequestForm()
        return render(request, 'payment-issue.html', {'requestform': form})

def report(request):
    if request.method == 'POST':
        filled_form = ReportForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            filled_form = ReportForm()
        return render(request, 'report-user.html', {'reportform': filled_form})
    else:
        form = ReportForm()
        return render(request, 'report-user.html', {'reportform': form})

def status(request):
    status_all_data = RaiseRequest.objects.all()
    return render(request, 'status.html', {'status':status_all_data})

def statussingle(request, id):
    link = id
    status_data = RaiseRequest.objects.get(id=link)
    print(status_data)
    return render(request, 'status.html',{'statusdata':status_data})


    