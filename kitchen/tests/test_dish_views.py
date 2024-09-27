from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish

LIST_URL = reverse("kitchen:dish-list")
CREATE_URL = reverse("kitchen:dish-create")
UPDATE_URL = reverse("kitchen:dish-update", kwargs={"pk": 1})
DELETE_URL = reverse("kitchen:dish-delete", kwargs={"pk": 1})
LOGIN_URL = reverse("login")


class PublicDishViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def test_list_view_login_required_and_redirect(self):
        response = self.client.get(LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={LIST_URL}")

    def test_create_view_login_required_and_redirect(self):
        response = self.client.get(CREATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={CREATE_URL}")

    def test_update_view_login_required_and_redirect(self):
        response = self.client.get(UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={UPDATE_URL}")

    def test_delete_view_login_required_and_redirect(self):
        response = self.client.get(DELETE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={DELETE_URL}")


class PrivateCarViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def setUp(self):
        self.client.force_login(get_user_model().objects.get(pk=1))

    def test_list_view_is_paginated_by_5(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("dish_list")), 5)

    def test_list_view_correct_num_of_entries_on_next_page(self):
        response = self.client.get(LIST_URL + "?page=20")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("dish_list")), 2)

    def test_list_view_context_contain_search_by_name_and_it_works(self):
        response = self.client.get(LIST_URL + "?name=cAr")
        dishes_ = list(response.context.get("dish_list").values("name"))
        custom_dishes = [
            {"name": "Baked Carp"},
            {"name": "Carbonara"},
            {"name": "Quattro Di Carne"},
            {"name": "Spaghetti Carbonara"},
        ]

        self.assertIn("search_form", response.context)
        self.assertTrue(len(dishes_) == 4)
        self.assertCountEqual(custom_dishes, dishes_)

    def test_create_view(self):
        data = {
            "name": "custom_dish",
            "description": "",
            "price": 88.88,
            "dish_type": 3,
            "cooks": [1, 2, 3],
        }

        response = self.client.post(CREATE_URL, data)

        self.assertRedirects(response, LIST_URL)
        self.assertTrue(Dish.objects.filter(name="custom_dish").exists())

    def test_update_view(self):
        data = {
            "name": "custom_dish",
            "description": "",
            "price": 88.88,
            "dish_type": 8,
            "cooks": [1, 2, 3],
        }
        before = Dish.objects.get(pk=1)

        response = self.client.post(UPDATE_URL, data)
        after = Dish.objects.get(pk=1)

        self.assertRedirects(response, LIST_URL)
        self.assertEqual(after.name, "custom_dish")
        self.assertEqual(after.dish_type.id, 8)
        self.assertEqual(after.price, Decimal("88.88"))
        self.assertEqual(after.id, before.id)

    def test_delete_view(self):
        response = self.client.post(DELETE_URL)

        self.assertRedirects(response, LIST_URL)
        self.assertFalse(Dish.objects.filter(pk=1).exists())
