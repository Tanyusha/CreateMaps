from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from customauth.forms import UserCreationForm
from django.conf.urls import patterns, url

__author__ = 'pahaz'


def registration(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        try:
            g = Group.objects.get(name='user')
        except Group.DoesNotExist:
            import init_db
            g = Group.objects.get(name='user')

        user.groups.add()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('profile')
    return render(request, 'registration.html', {'form': form})


urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^register/$', registration, name='registration')
)
