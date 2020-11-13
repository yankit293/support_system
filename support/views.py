from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import HttpResponse
from .form import RequestForm, ReportForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from .models import RaiseRequest


def index(request):
    return render(request, 'support.html')

def payment(request):
    if request.method == 'POST':
        filled_form = RequestForm(request.POST, request.FILES)
        if filled_form.is_valid():

            filled_form.save()
            note = 'Thanks for sending request!'
            filled_form = RequestForm()
            return render(request, 'status.html', {'note': note})
        else:
            status_data = RaiseRequest.object.filter(email = cleaned_data['email'])
            """ note = 'This issue is already created'
            return render(request, 'status.html', {'note': note}) """
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
    """ email = filled_form.cleaned_data['email']
    status_data = RaiseRequest.objects.filter(email=email)
    print(status_data) """
    return render(request, 'status.html')

""" def status(request):
    email = filled_form.cleaned_data['email'] 
    email = 
    status_data = RaiseRequest.objects.filter(email=email)
    print(status_data)
    return render(request, 'status.html',{'statusdata':status_data}) """


'''def SendMail():
    name = filled_form.cleaned_data['name']
    sender = filled_form.cleaned_data['email']
    issue = filled_form.cleaned_data['issue']
    subject = "{}:{} request at Piblitz".format(name,issue)
    html_message = render_to_string('email-inlined.html',{'name':name})
    plain_message = strip_tags(html_message)
    recipient = []
    recipient.append(sender)
    return send_mail(subject,plain_message,from_email=None, recipient_list=recipient,html_message=html_message,fail_silently=False,)'''