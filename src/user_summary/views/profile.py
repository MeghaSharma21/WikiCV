from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This file contains sample code to test authentication using OAuth


def index(request):
    context = {}
    return render(request, 'user_summary/index.html', context)


@login_required()
def profile(request):
    context = {}
    return render(request, 'user_summary/profile.html', context)


def login_oauth(request):
    context = {}
    return render(request, 'user_summary/login.html', context)
