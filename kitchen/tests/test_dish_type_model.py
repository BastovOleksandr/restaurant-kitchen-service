from django.core.management import call_command
from django.test import TestCase

from kitchen.models import DishType


class DishTypeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def test_object_to_str(self):
        dish_type = DishType.objects.get(id=1)

        self.assertEqual(
            str(dish_type), f'dish type: "{dish_type.name}"'
        )

    def test_query_set_should_be_ordered_by_name(self):
        unordered_names = ["Bab", "Bca", "Abc"]
        for name in unordered_names:
            DishType.objects.create(name=name)
        names = [
            dish_type.name
            for dish_type in DishType.objects.all()[:3]
        ]

        self.assertEqual(names, ["Abc", "Bab", "Bca"])

    def test_name_field_max_length(self):
        dish_type = DishType.objects.get(id=1)
        max_length = dish_type._meta.get_field("name").max_length

        self.assertEqual(max_length, 255)
