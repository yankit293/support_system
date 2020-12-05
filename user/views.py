from django.shortcuts import render, redirect
from .form import CreateUserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages




def register(request):
    if request.method == 'POST':
        registerform = CreateUserForm(request.POST)
        if registerform.is_valid():
            registerform.save()
            registerform = CreateUserForm()
        return render(request, 'registeration.html',{ 'form':registerform })
    else:
        registerform = CreateUserForm()
        return render(request, 'registeration.html',{ 'form':registerform })

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/support')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/support")