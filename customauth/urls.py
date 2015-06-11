from django import forms
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from customauth.forms import UserCreationForm
from customauth.models import MyUser
from maps.models import Map

__author__ = 'pahaz'

from django.conf.urls import patterns, url


def registration(request):
    form = UserCreationForm(request.POST)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.groups.add(Group.objects.get(name='user'))
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('admin:index')
    return render(request, 'registration.html', {'form': form})

urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', registration, name='registration')
)
