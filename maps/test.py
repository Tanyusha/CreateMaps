import unittest
from maps.yandex import create_yandex_point_object

__author__ = 'Таника'


class YandexPointTest(unittest.TestCase):
    def test_info_about_objects(self):
        z = create_yandex_point_object(1, [2,3], a="test1", b="test2", c="test3")
        self.assertEqual(z['properties']['balloonContent'], "<p><strong>a:</strong>test1</p>"
                                                            "<p><strong>b:</strong>test2</p>"
                                                            "<p><strong>c:</strong>test3</p>")