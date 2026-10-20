from django.test import TestCase
from .models import Direction


class BasicTest(TestCase):
    def test_direction_str(self):
        d = Direction.objects.create(name='Тест', slug='test')
        self.assertEqual(str(d), 'Тест')
