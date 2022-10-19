from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import AuthenticationForm, NewUserForm


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                messages.success(request, "Thank you for signing up. You can Login!")
                return redirect('signin')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()

    return render(request=request, template_name='authentication/signup.html', context={"form": form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username.upper()}.")
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="authentication/signin.html", context={"form": form})


def signout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')
