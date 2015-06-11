import string

from collections import OrderedDict
from _project_.utils import add_db_to_request
from core.database import TableType
from core.django_form_factory import make_form
from core.load_objects import dumps
from core.utils import make_inner_paths_for_table
from customauth.urls import registration
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.storage import get_storage_class
from maps.models import Map, Dataset, Field
from maps.utils import dump_map_objs, load_map_objs
from maps.yandex import create_yandex_poinrs_objects
import os
from core import DATABESE_TYPES
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render, redirect
from django import forms
from django.core.cache import cache
import random

STORAGE = get_storage_class()()
STEP_6_QUERY = 'step-6-query'
STEP_7_LAT = "step-7-latitude-column"
STEP_7_LON = "step-7-longitude-column"
REDIRECT_IF_NO_QUERY = 'step3'
STEP_8_ATTRS = 'step-8-attrs'
STEP_3_MAP = "step-3-map-id"
STEP_3_DATASET = "step-3-dataset-id"


class UploadFile(forms.Form):
    file = forms.FileField()


def index(request):
    # if request.user.is_authenticated():
    #     return redirect('admin:index')
    return render(request, 'index.html', {'maps': Map.objects.all()})


def login(request):
    return redirect('admin:index')


def logout(request):
    return redirect('admin:logout')


def user(request):
    if not request.user.is_authenticated():
        return redirect('index')
    return render(
        request, 'user.html',
        {'maps': request.user.editable_maps.all()}
    )


def map(request, id):
    m = Map.objects.get(id=id)
    d = load_map_objs(m)
    y = dumps(create_yandex_poinrs_objects(d))
    return render(request, 'map.html', {'map': m, 'objects': d, 'yandex': y})


@login_required
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
    return render(request, 'create-1.html',
                  {'databases': DATABESE_TYPES.keys(), 'form': form})


@login_required
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
    maps = request.user.editable_maps.all()
    errors = []
    if request.method == "POST":
        if 'map' not in request.POST:
            errors.append('Выберите карту или создайте новую')
        else:
            map = request.POST.get('map')
            if map == 'new':
                description = request.POST.get('map-description')
                name = request.POST.get('map-name')
                m = Map(name=name, description=description,
                        user=request.user)
                m.save()
                m.editors.add(request.user)
                map = m
            else:
                map = Map.objects.get(id=int(map))

            if not request.POST.get('dataset-name'):
                dataset_name = ''.join([random.choice(string.hexdigits)
                                        for _ in range(10)])
            else:
                dataset_name = request.POST['dataset-name']

            dataset = Dataset.objects.create(name=dataset_name, map=map)
            dataset.save()

            request.session[STEP_3_MAP] = map.id
            request.session[STEP_3_DATASET] = dataset.id
            return redirect('step3next')
    return render(request, 'create-3.html', {'maps': maps, 'errors': errors})


@add_db_to_request
def create_step_3_next(request):
    return render(request, 'create-3-next.html')


@add_db_to_request
def create_step_4_0(request):
    db = request.db
    tables = [x for x in db.tables(TableType.TABLE).values()]

    error = ""
    if request.method == "POST":
        if 'table' in request.POST:
            request.session["step-4-selected-table"] = request.POST['table']
            return redirect('step5')
        else:
            error = "Вы не выбрали главную таблицу"
            return render(request, 'create-4-0.html',
                          {'tables': tables, 'error': error})

    return render(request, 'create-4-0.html',
                  {'tables': tables, 'error': error})


@add_db_to_request
def create_step_6_a_1(request):
    query = request.session.get(STEP_6_QUERY, '')
    db = request.db
    tables = [x for x in db.tables(TableType.TABLE).values()]
    errors = []
    result, cols = [], []
    has_next = False
    if request.method == "POST":
        query = request.POST.get('query', '')
        next = request.POST.get('next')
        if not query:
            errors.append('Введите запрос')
        else:
            try:
                result, cols = request.db.execute(query)
                has_next = True
                request.session[STEP_6_QUERY] = query
            except Exception as e:
                errors.append(e)

    return render(request, 'create-6-a-1.html',
                  {'query': query, 'errors': errors, 'tables': tables,
                   'has_next': has_next, 'result': result, 'cols': cols,
                   'results': len(result)})


@add_db_to_request
def create_step_6_b_1(request):
    db = request.db
    tables = [x for x in db.tables(TableType.TABLE).values()]

    error = ""
    if request.method == "POST":
        if 'table' in request.POST:
            request.session["step-6-selected-table"] = request.POST['table']
            return redirect('step62')
        else:
            error = "Вы не выбрали таблицу с основной информацией об объектах"
            return render(request, 'create-5.html',
                          {'tables': tables, 'error': error})
    return render(request, 'create-6-b-1.html',
                  {'tables': tables, 'error': error})


def cached_db_data(db_filename, selected_table, db):
    cache_key = 'db.paths:' + db_filename + ":" + selected_table
    d = cache.get(cache_key)
    if d is not None:
        return d

    tables = db.tables()
    relationships_inner, relations_outer = db.relationships()
    paths, used_tables = make_inner_paths_for_table(selected_table, tables,
                                                    relationships_inner)
    d = tables, relationships_inner, relations_outer, paths, used_tables
    cache.set(cache_key, d)
    return d


@add_db_to_request
def create_step_6_b_2(request):
    selected_table = request.session.get("step-6-selected-table")
    if not selected_table:
        return redirect('step61')

    latitude = request.session.get(STEP_7_LAT)
    longitude = request.session.get(STEP_7_LON)
    if not latitude or not longitude:
        return redirect('step3')

    db = request.db
    db_filename = request.db_filename
    tables, relationships_inner, relations_outer, paths, used_tables = cached_db_data(
        db_filename, selected_table, db)

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

    return render(request, 'create-6-b-2.html', {
        'paths': path_strings, 'errors': [], 'tree': tree,
        'table_info_links': table_info_links
    })


@add_db_to_request
def create_step_7(request):
    query = request.session.get(STEP_6_QUERY)
    if not query:
        return redirect(REDIRECT_IF_NO_QUERY)

    result, cols = request.db.execute(query)
    selected_table_columns = [x[0] for x in cols]
    lat = request.session.get(STEP_7_LAT)
    lon = request.session.get(STEP_7_LON)

    error = ""
    LAT_KEY = 'lat'
    LON_KEY = 'lon'
    if request.method == "POST":
        if LAT_KEY in request.POST:
            if LON_KEY in request.POST:
                latitude = request.POST.get(LAT_KEY)
                longitude = request.POST.get(LON_KEY)

                if latitude not in selected_table_columns or longitude not in selected_table_columns:
                    error = "Столбцов нет в выборке"
                else:
                    request.session[STEP_7_LAT] = selected_table_columns.index(
                        latitude)
                    request.session[STEP_7_LON] = selected_table_columns.index(
                        longitude)
                    return redirect('step8')
            else:
                error = "Вы не указали долготу объектов"
        else:
            if LON_KEY in request.POST:
                error = "Вы не указали широту объектов"
            else:
                error = "Вы не указали координаты объектов"

    return render(request, 'create-7.html',
                  {'cols': selected_table_columns, 'error': error,
                   'lat': lat, 'lon': lon})


@add_db_to_request
def create_step_8(request):
    query = request.session.get(STEP_6_QUERY)
    if not query:
        return redirect(REDIRECT_IF_NO_QUERY)

    lat = request.session[STEP_7_LAT]
    lon = request.session[STEP_7_LON]
    result, cols = request.db.execute(query)
    selected_table_columns = [x[0] for x in cols]
    attrs = [[0, 0, i, 0, x[0]] for i, x in enumerate(cols)]
    # attrs = request.session.get(STEP_8_ATTRS, d_attrs)
    REQUIRED = 0
    FILTER = 1
    INDEX = 2
    DISABLED = 3
    NAME = 4

    attrs[lat][DISABLED] = 1
    attrs[lat][FILTER] = 1
    attrs[lat][REQUIRED] = 1
    attrs[lon][DISABLED] = 1
    attrs[lon][FILTER] = 1
    attrs[lon][REQUIRED] = 1

    error = []
    if request.method == "POST":
        for key, value in request.POST.items():
            value = True if value == 'on' else False
            if key.endswith('-filter'):
                key = key[:-len('-filter')]
                attrs[selected_table_columns.index(key)][
                    FILTER] = 1 if value else 0
            elif key.endswith('-required'):
                key = key[:-len('-required')]
                attrs[selected_table_columns.index(key)][
                    REQUIRED] = 1 if value else 0

        if not error:
            request.session[STEP_8_ATTRS] = attrs
            map_id = request.session[STEP_3_MAP]
            dataset_id = request.session[STEP_3_DATASET]
            map = Map.objects.get(id=map_id)
            for req, filter, index, disable, name in attrs:
                f = Field(map=map, name=name, is_required=req,
                          is_filter=filter)
                f.save()

            return redirect('step10')

    return render(request, 'create-8.html',
                  {'cols': attrs, 'error': error,
                   'lat': lat, 'lon': lon})


@add_db_to_request
def create_9(request):
    return render(request, 'create-9.html')


@add_db_to_request
def create_step_10(request):
    query = request.session.get(STEP_6_QUERY)
    if not query:
        return redirect(REDIRECT_IF_NO_QUERY)

    lat = request.session[STEP_7_LAT]
    lon = request.session[STEP_7_LON]
    map_id = request.session[STEP_3_MAP]
    dataset_id = request.session[STEP_3_DATASET]
    map = Map.objects.get(id=map_id)
    dataset = Dataset.objects.get(id=dataset_id)

    result, cols = request.db.execute(query)
    selected_table_columns = [x[0] for x in cols]
    objs = load_map_objs(map)

    for row in result:
        try:
            longitude = float(row[lon])
        except:
            longitude = None
        try:
            latitude = float(row[lat])
        except:
            latitude = None
        data = {}

        for i, v in enumerate(row):
            if i in [lat, lon]:
                continue
            data[selected_table_columns[i]] = v

        d = {'lat': latitude, 'lon': longitude, 'data': data}
        objs.append(d)

        # m = MObject.objects.create(map=map, dataset=dataset,
        #                            lon=longitude,
        #                            lat=latitude,
        #                            data=data)
        # print(m.id)

    dump_map_objs(map, objs)

    del request.session[STEP_7_LAT]
    del request.session[STEP_7_LON]
    del request.session[STEP_8_ATTRS]
    del request.session[STEP_3_DATASET]
    del request.session[STEP_3_MAP]
    return render(request, 'create-10.html')


urlpatterns = [
    # Examples:
    # url(r'^$', '_project_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^map/(\d+)$', map, name='map'),
    url(r'^$', index, name='index'),
    url(r'^create-1$', create_step_1, name='step1'),
    url(r'^create-2$', create_step_2, name='step2'),
    url(r'^create-3$', create_step_3, name='step3'),
    url(r'^create-3-next$', create_step_3_next, name='step3next'),
    url(r'^create-4-0$', create_step_4_0, name='step40'),
    url(r'^create-6-a-1$', create_step_6_a_1, name='step6a1'),
    url(r'^create-6-b-1$', create_step_6_b_1, name='step6b1'),
    url(r'^create-6-b-2$', create_step_6_b_2, name='step6b2'),
    url(r'^create-7$', create_step_7, name='step7'),
    url(r'^create-8$', create_step_8, name='step8'),
    url(r'^create-10$', create_step_10, name='step10'),
    # url(r'^registration$', registration, name='registration'),
    # url(r'^login$', login, name='login'),
    # url(r'^logout$', logout, name='logout'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', registration, name='registration'),

    url(r'^user/$', user, name='profile'),
    url(r'^admin/', include(admin.site.urls)),
]
