from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType

INDEX_URL = reverse("kitchen:index")


class PublicIndexViewTests(TestCase):
    def test_login_not_required_(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)


class PrivateIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def setUp(self):
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)

    def test_should_use_defined_template(self):
        self.assertTemplateUsed(
            self.client.get(INDEX_URL), "kitchen/index.html"
        )

    def test_context_contains_correct_data(self):
        response = self.client.get(INDEX_URL)
        cooks = get_user_model().objects.count()
        dishes = Dish.objects.count()
        dish_types = DishType.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("num_cooks"), cooks)
        self.assertEqual(response.context.get("num_dishes"), dishes)
        self.assertEqual(response.context.get("num_dish_types"), dish_types)
