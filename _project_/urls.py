from core.django_form_factory import make_form
import os
from core import DATABESE_TYPES
from django.conf.urls import include, url
from django.contrib import admin
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
import tempfile


class UploadFile(forms.Form):
    file = forms.FileField()


def index(request):
    return render(request, 'index.html')


def create_step_1(request):
    form = UploadFile(request.POST, request.FILES)
    if request.method == "POST" and form.is_valid():
        f = request.FILES['file']
        destination = tempfile.NamedTemporaryFile(delete=False)
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        request.session['step-1-filepath'] = destination.name
        request.session['step-1-filename'] = f.name
        return redirect('step2')
    return render(request, 'create-1.html', {'databases': DATABESE_TYPES.keys(), 'form': form})


def create_step_2(request):
    filename = request.session.get('step-1-filename')
    file = request.session.get('step-1-filepath')

    name, ext = os.path.splitext(filename)
    DBase = DATABESE_TYPES.get(ext)
    if not DBase:
        return render(request, 'error-db-not-supported.html')

    fields = DBase.required_info_for_init()
    Form = make_form(fields)
    POST = request.POST.copy()
    POST.update({'file': file})
    form = Form(POST)
    if request.method == "POST" and form.is_valid():
        try:
            data = form.cleaned_data
            db = DBase(**data)
            db.close()
            request.session['step-2-database-init-data'] = data
            request.session['step-2-database'] = ext
        except Exception as e:
            form.add_error(None, str(e))
        else:
            return redirect('step3')

    return render(request, 'create-2.html', {'form': form})


def create_step_3(request):
    form = forms.BaseForm
    data = request.session.get('step-2-database-init-data')
    ext = request.session.get('step-2-database')
    DBase = DATABESE_TYPES.get(ext)
    if not DBase:
        return render(request, 'error-db-not-supported.html')

    db = DBase(**data)
    tables = db.tables()
    db.close()

    # for table in tables:
    #     print(tables[table].name)
    #     for column in tables[table].columns:
    #         print(column.name)
        #     column_list.append(column.name)
        # tables_list['tables[table].name']=column_list
    if request.method == "POST":
        request.session["step-3-selected-table"] = request.POST['table']
        return redirect('step4')
    return render(request, 'create-3.html', {'tables': tables})


def create_step_4(request):
    ext = request.session.get('step-2-database')
    data = request.session.get('step-2-database-init-data')
    selected_table = request.session["step-3-selected-table"]

    DBase = DATABESE_TYPES.get(ext)
    db = DBase(**data)
    tables = db.tables()
    db.close()
    column_list = []
    for table in tables:
        print(table)
        if table == selected_table:
            for column in tables[table].columns:
                column_list.append(column.name)
            break
    if request.method == "POST":
        request.session["step-4-coord-X"] = request.POST['coord-X']
        request.session["step-4-coord-Y"] = request.POST['coord-Y']
        return redirect('step5')
    return render(request, 'create-4.html', {'table': selected_table, 'columns': column_list})

def create_step_5(request):
    ext = request.session.get('step-2-database')
    coord_x = request.session.get("step-4-coord-X")
    coord_y = request.session.get("step-4-coord-Y")

    return render(request, 'create-5.html', {'coord_X': coord_x, 'coord_Y': coord_y})

urlpatterns = [
    # Examples:
    # url(r'^$', '_project_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^map$', index),
    url(r'^$', create_step_1),
    url(r'^create-1$', create_step_1, name='step1'),
    url(r'^create-2$', create_step_2, name='step2'),
    url(r'^create-3$', create_step_3, name='step3'),
    url(r'^create-4$', create_step_4, name='step4'),
    url(r'^create-5$', create_step_5, name='step5'),
    url(r'^admin/', include(admin.site.urls)),
]
