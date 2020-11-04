from django.shortcuts import render
from django.http import HttpResponse
from .form import RequestForm
from .models import RaiseRequest


def index(request):
    if request.method == 'POST':
        filled_form = RequestForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            note = 'Thanks for sending request!'
            filled_form = RequestForm()
        else:
            note = 'Information is not valid'
        return render(request, 'support.html', {'requestform': filled_form, 'note': note})
    else:
        form = RequestForm()
        return render(request, 'support.html', {'requestform': form})