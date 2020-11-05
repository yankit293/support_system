from django.shortcuts import render
from django.http import HttpResponse
from .form import RequestForm, ReportForm

def index(request):
    return render(request, 'support.html')

def payment(request):
    if request.method == 'POST':
        filled_form = RequestForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            note = 'Thanks for sending request!'
            filled_form = RequestForm()
        else:
            note = 'Information is not valid'
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