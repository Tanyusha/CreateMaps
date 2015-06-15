from __future__ import unicode_literals, print_function, generators, division
from _project_.consts import STEP_3_MAP, STEP_3_DATASET
from _project_.utils import generate_random_string
from customauth.models import MyUser
from maps.models import Dataset, Map
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

__author__ = 'pahaz'
TEST_DATABASE = os.path.join(settings.BASE_DIR, 'base.mdb')
MAP_DESCRIPTION = "Карта содержит информацию о месторождениях {0} области"
MAP_NAME = "Полезные ископаемые {0} области"
DATASET_NAME = "set-{0}"
QUERY = '''SELECT DISTINCT ОПИ_Участки.Наименование AS [Наименование участка],
 ОПИ_Участки.[Целевое назначение], ОПИ_Участки.[Координата-широта],
 ОПИ_Участки.[Координата-долгота], ОПИ_Участки.[Дата изменения],
 ОПИ_УчасткиОПИ.[Глубина запасов], Спр_ОПИ.НаименованиеОПИ AS
 [Наименование ОПИ], ОПИ_Месторождения.Наименование AS
 [Наименование месторождения]
FROM Спр_ОПИ INNER JOIN ((ОПИ_УчасткиОПИ INNER JOIN ОПИ_Участки ON ОПИ_УчасткиОПИ.ИДУчастка = ОПИ_Участки.ИДУчастка)
INNER JOIN ОПИ_Месторождения ON ОПИ_Участки.ИДМесторождения = ОПИ_Месторождения.ИДМесторождения) ON Спр_ОПИ.КодОПИ = ОПИ_УчасткиОПИ.КодОПИ
WHERE ОПИ_Участки.[Координата-долгота] is not null and ОПИ_Участки.[Координата-широта] is not null
and ОПИ_Участки.[Координата-долгота] <> '' and ОПИ_Участки.[Координата-широта] <> ''
'''
LON = "координата-долгота"
LAT = "координата-широта"
FILTERS = {
    "наименование участка-filter": 'on',
    "целевое назначение-filter": 'on',
    "дата изменения-filter": 'on',
    "глубина запасов-filter": 'on',
    "наименование опи-filter": 'on',
    "наименование месторождения-filter": 'on',
}

FIELDS = [
    "наименование участка",
    "целевое назначение",
    "дата изменения",
    "глубина запасов",
    "наименование опи",
    "наименование месторождения",
]


class CreateTestCase(TestCase):
    def login_or_register(self, username='test', password='test'):
        r = self.client.post(reverse("login"), {
            'username': username, 'password': password,
        })

        if r.context and r.context['form'].errors:
            r = self.client.post(reverse('registration'), {
                'username': username, 'password1': password,
                'password2': password,
                'email': username + '@ex.com'
            })

        self.assertRedirects(r, reverse('profile'))

    def get_user(self):
        user_id = self.client.session['_auth_user_id']
        return MyUser.objects.get(id=user_id)

    def test_create(self):
        self.login_or_register()
        p1 = self.client.get(reverse('step1'))
        self.assertEqual(p1.status_code, 200)
        with open(TEST_DATABASE, 'rb') as f:
            p2 = self.client.post(reverse('step1'), {'file': f})
        self.assertRedirects(p2, reverse('step2'))

        print(self.client.session.items())

        # step 2

        p1 = self.client.get(reverse('step2'))
        self.assertEqual(p1.status_code, 200)
        p2 = self.client.post(reverse('step2'), {
            'username': 'Admin',
            'password': 'Masterkey1'
        })
        self.assertRedirects(p2, reverse('step3'))

        print(self.client.session.items())

        # step 3

        p1 = self.client.get(reverse('step3'))
        self.assertEqual(p1.status_code, 200)
        name = 'test-' + generate_random_string(10)
        map_name = MAP_NAME.format(name)
        map_description = MAP_DESCRIPTION.format(name)
        ds_name = DATASET_NAME.format(name)
        p2 = self.client.post(reverse('step3'), {
            'map': 'new',
            'map-name': map_name,
            'map-description': map_description,
            'dataset-name': ds_name,
        })
        self.assertRedirects(p2, reverse('step4'))

        print(3, self.client.session.items())

        map_id = self.client.session[STEP_3_MAP]
        dataset_id = self.client.session[STEP_3_DATASET]
        map = Map.objects.get(id=map_id)
        ds = Dataset.objects.get(id=dataset_id)
        user = self.get_user()
        self.assertMap(map, map_name, map_description, user.id, [user.id])
        self.assertDataset(ds, ds_name, map.id)

        # step4 Point

        TYPE = 'Point'
        p1 = self.client.get(reverse('step4'))
        self.assertEqual(p1.status_code, 200)
        p2 = self.client.post(reverse('step4'), {
            'type': TYPE
        })
        self.assertRedirects(p2, reverse('step5'))

        print(4, self.client.session.items())

        # step5

        p1 = self.client.get(reverse('step5'))
        self.assertEqual(p1.status_code, 200)
        self.assertInHTML('<a href="{0}">Ввести запрос</a>'
                          .format(reverse('step6a1')),
                          p1.content.decode())

        # step6 A 1

        p1 = self.client.get(reverse('step6a1'))
        self.assertEqual(p1.status_code, 200)
        p2 = self.client.post(reverse('step6a1'), {
            'query': QUERY,
        })
        self.assertEqual(p2.status_code, 200)
        self.assertEqual(p2.context['has_next'], True)

        print('6a1', self.client.session.items())

        # step7

        p1 = self.client.get(reverse('step7'))
        self.assertEqual(p1.status_code, 200)
        p2 = self.client.post(reverse('step7'), {
            'lon': LON,
            'lat': LAT,
        })
        self.assertRedirects(p2, reverse('step8'))

        print(7, self.client.session.items())

        # step8

        p1 = self.client.get(reverse('step8'))
        self.assertEqual(p1.status_code, 200)
        p2 = self.client.post(reverse('step8'), FILTERS)
        self.assertRedirects(p2, reverse('step10'),
                             fetch_redirect_response=False)

        print(8, self.client.session.items())

        self.assertMapFields(map, FIELDS)

        # step10

        p = self.client.get(reverse('step10'))
        self.assertIn('a href="{0}"'.format(reverse('map', args=(map_id,))),
                      p.content.decode())
        print(10, self.client.session.items())

    def assertMap(self, map, map_name, map_description, user_id, editors):
        self.assertEqual(map.name, map_name)
        self.assertEqual(map.description, map_description)
        self.assertEqual(map.user_id, user_id)
        self.assertEqual([x.id for x in map.editors.all()], editors)

    def assertDataset(self, dataset, dataset_name, map_id):
        self.assertEqual(dataset.name, dataset_name)
        self.assertEqual(dataset.map_id, map_id)

    def assertMapFields(self, map, fields):
        self.assertEqual([x.name for x in map.fields.all()], fields)
