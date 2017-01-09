import requests
from django.contrib import messages
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'index.html')


@csrf_protect
def complete_auth(request):
    messages.success(request, 'Добро пожаловать, %s!' % request.session['email'])
    return redirect('/event/map/')


def sign_in(request):
    if request.user.is_authenticated():
        return redirect('/event/map/')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/event/map/')
