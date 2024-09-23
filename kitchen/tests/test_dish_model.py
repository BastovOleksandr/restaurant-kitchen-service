from django.core.management import call_command
from django.db import models
from django.test import TestCase

from kitchen.models import Dish, DishType, Cook


class DishModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def setUp(self):
        self.dish = Dish.objects.get(id=1)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), f'dish: "{self.dish.name}"')

    def test_name_field_max_length(self):
        max_length = self.dish._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_dish_type_field(self):
        field = Dish._meta.get_field("dish_type")

        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.related_model, DishType)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_drivers_field(self):
        field = Dish._meta.get_field("cooks")

        self.assertTrue(isinstance(field, models.ManyToManyField))
        self.assertEqual(field.related_model, Cook)
        self.assertEqual(field.remote_field.related_name, "dishes")
