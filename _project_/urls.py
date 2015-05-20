from collections import OrderedDict
from _project_.utils import add_db_to_request
from core.database import TableType
from core.django_form_factory import make_form
from core.utils import make_inner_paths_for_table
from django.core.files import File
from django.core.files.storage import get_storage_class
import os
from core import DATABESE_TYPES
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render, redirect
from django import forms
from django.core.cache import cache


STORAGE = get_storage_class()()


class UploadFile(forms.Form):
    file = forms.FileField()


def index(request):
    return render(request, 'index.html')


def registration(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')


def user(request):
    return render(request, 'user.html')


def map(request):
    return render(request, 'map.html')


def create_step_1(request):
    if request.method == "POST":
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            ff = File(f, f.name)
            path = STORAGE.save(f.name, ff)
            request.session['step-1-filepath'] = path
            return redirect('step2')
    else:
        form = UploadFile()
    return render(request, 'create-1.html', {'databases': DATABESE_TYPES.keys(), 'form': form})


def create_step_2(request):
    path = request.session.get('step-1-filepath')
    path = STORAGE.path(path)
    name = os.path.basename(path)

    name, ext = os.path.splitext(name)
    DBase = DATABESE_TYPES.get(ext)
    if not DBase:
        return render(request, 'error-db-not-supported.html')

    fields = DBase.required_info_for_init()
    Form = make_form(fields)

    if request.method == "POST":
        POST = request.POST.copy()
        POST.update({'file': path})

        form = Form(POST)
        if form.is_valid():
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
    else:
        form = Form()

    return render(request, 'create-2.html', {'form': form})

@add_db_to_request
def create_step_3(request):
    # if request.method == "POST":
    #     return render(request, 'create-4.html')
    return render(request, 'create-3.html')

@add_db_to_request
def create_step_4(request):
    db = request.db
    tables = [x for x in db.tables(TableType.TABLE).values()]

    error = ""
    if request.method == "POST":
        if 'table' in request.POST:
            request.session["step-4-selected-table"] = request.POST['table']
            return redirect('step5')
        else:
            error = "Вы не выбрали таблицу с координатами"
            return render(request, 'create-4.html', {'tables': tables, 'error': error})
    return render(request, 'create-4.html', {'tables': tables, 'error': error})


@add_db_to_request
def create_step_5(request):
    selected_table = request.session.get("step-4-selected-table")
    if not selected_table:
        return redirect('step4')

    db = request.db
    tables = db.tables(TableType.TABLE)

    selected_table = tables.get(selected_table)
    selected_table_columns = [x.name for x in selected_table.columns]
    if not selected_table:
        return render(request, 'error-db-wrong-selected-table.html')

    error = ""
    LAT_KEY = 'lat'
    LNG_KEY = 'lng'
    if request.method == "POST":
        if LAT_KEY in request.POST:
            if LNG_KEY in request.POST:
                latitude = request.POST.get(LAT_KEY)
                longitude = request.POST.get(LNG_KEY)

                if latitude not in selected_table_columns or longitude not in selected_table_columns:
                    error = "Столбцов нет в таблице"
                else:
                    request.session["step-5-latitude-column"] = latitude
                    request.session["step-5-longitude-column"] = longitude
                    return redirect('step6')
            else:
                error = "Вы не указали долготу объектов"
        else:
            if LNG_KEY in request.POST:
                error = "Вы не указали широту объектов"
            else:
                error = "Вы не указали координаты объектов"

    return render(request, 'create-5.html', {'table': selected_table, 'error': error})


@add_db_to_request
def create_step_6(request):
    db = request.db
    tables = [x for x in db.tables(TableType.TABLE).values()]

    error = ""
    if request.method == "POST":
        if 'table' in request.POST:
            request.session["step-6-selected-table"] = request.POST['table']
            return redirect('step7')
        else:
            error = "Вы не выбрали таблицу с основной информацией об объектах"
            return render(request, 'create-5.html', {'tables': tables, 'error': error})
    return render(request, 'create-6.html', {'tables': tables, 'error': error})

def cached_db_data(db_filename, selected_table, db):
    cache_key = 'db.paths:' + db_filename + ":" + selected_table
    d = cache.get(cache_key)
    if d is not None:
        return d

    tables = db.tables()
    relationships_inner, relations_outer = db.relationships()
    paths, used_tables = make_inner_paths_for_table(selected_table, tables, relationships_inner)
    d = tables, relationships_inner, relations_outer, paths, used_tables
    cache.set(cache_key, d)
    return d


@add_db_to_request
def create_step_7(request):
    selected_table = request.session.get("step-6-selected-table")
    if not selected_table:
        return redirect('step6')

    latitude = request.session.get("step-5-latitude-column")
    longitude = request.session.get("step-5-longitude-column")
    if not latitude or not longitude:
        return redirect('step5')

    db = request.db
    db_filename = request.db_filename
    tables, relationships_inner, relations_outer, paths, used_tables = cached_db_data(db_filename, selected_table, db)

    tree = OrderedDict()
    for index, path in enumerate(paths):
        current_dict = tree
        last_index = len(path) - 1
        for i, p in enumerate(path):
            if i == last_index:
                current_dict[p.name] = OrderedDict()
            else:
                current_dict = current_dict[p.table_fk]

    path_strings = []
    connections = {}

    for path in paths:
        last_index = len(path) - 1
        current_path = ''
        for i, p in enumerate(path):
            if i == last_index:
                current_path += p.name
            else:
                current_path += p.table_fk + ' -> '
        path_strings.append(current_path)

    print(used_tables)

    outer_tables_links = {}
    for x in used_tables:
        rs = relations_outer.get(x, [])
        for r in rs:
            if r.table in used_tables:
                continue
            # ('table', 'table_fk', 'relation_table', 'relation_table_pk')
            outer_tables_links.setdefault(r.table, set())
            outer_tables_links[r.table].add(r.relation_table)

    table_info_links = []
    for table, links in outer_tables_links.items():
        info = tables[table]
        rs = relations_outer.get(table, [])
        table_info_links.append((info, rs, links))

    return render(request, 'create-7.html', {'paths': path_strings, 'errors': [], 'tree': tree, 'table_info_links': table_info_links})


urlpatterns = [
    # Examples:
    # url(r'^$', '_project_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^map$', map),
    url(r'^$', index),
    url(r'^create-1$', create_step_1, name='step1'),
    url(r'^create-2$', create_step_2, name='step2'),
    url(r'^create-3$', create_step_3, name='step3'),
    url(r'^create-4$', create_step_4, name='step4'),
    url(r'^create-5$', create_step_5, name='step5'),
    url(r'^create-6$', create_step_6, name='step6'),
    url(r'^create-7$', create_step_7, name='step7'),
    url(r'^registration$', registration, name='registration'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^user$', user, name='user'),
    url(r'^admin/', include(admin.site.urls)),
]
