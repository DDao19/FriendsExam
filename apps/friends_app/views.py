# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from .models import User, Friend

# Create your views here.
def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)

def current_user(request):
    return User.objects.get(id=request.session['user_id'])


def index(request):

    return render(request, 'friends_app/index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.validate_registration(request.POST)
        if not errors:
            user = User.objects.create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully logged in!")
            return redirect(reverse('dashboard'))

        flash_errors(errors, request)

    return redirect(reverse('landing'))

def login(request):
    if request.method == "POST":
        result = User.objects.validate_login(request.POST)
        if type(result) == list:
            for err in result:
                messages.error(request, err)
            return redirect(reverse('landing'))
        request.session['user_id'] = result.id
        messages.success(request, "Successfully logged in!")
    return redirect(reverse('dashboard'))

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))

def dashboard(request):
    if 'user_id' in request.session:
        user = current_user(request)
        other_users = User.objects.exclude(id=request.session['user_id'])
        add_friend = Friend.objects.exclude(favorites=user)
        context = {
            'user': user,
            'add_friend': add_friend,
            'other_users': other_users,
            'favorites': user.favorites.all(),
        }
        return render(request, 'friends_app/dashboard.html', context)

    return redirect(reverse('landing'))


def favorite(request, id):
    user = current_user(request)
    favorite = User.objects.get(id=id)

    user.favorites.add(favorite)

    return redirect(reverse('dashboard'))

def remove(request, id):
    user = current_user(request)
    favorite = Friend.objects.get(id=id)
    user.favorites.remove(favorite)

    return redirect(reverse('dashboard'))

def show(request, id):

    user = User.objects.get(id=id)
    context = {
        'user': user,
        'favorites': user.favorites.all()
    }

    return render(request, 'friends_app/users.html', context)
