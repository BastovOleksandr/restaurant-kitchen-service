from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup


class AdminSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def setUp(self):
        self.admin_user = get_user_model().objects.first()
        self.client.force_login(self.admin_user)

    def test_cook_years_of_experience_listed(self):
        url = reverse("admin:kitchen_cook_changelist")

        response = self.client.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        years_of_experience_count = len(
            soup(text=str(self.admin_user.years_of_experience))
        )

        self.assertContains(response, "Years of experience")
        self.assertEqual(years_of_experience_count, 2)

    def test_cook_search_field_only_on_cook_list_page_and_works(self):
        url = reverse("admin:kitchen_cook_changelist") + "?q=w"

        response = self.client.get(url)

        self.assertContains(response, 'name="q"', count=1)
        self.assertContains(response, "Brown")
        self.assertContains(response, "Wilson")
        self.assertContains(response, "Walker")

    def test_cook_additional_fields_on_create_page(self):
        url = reverse("admin:kitchen_cook_add")
        additional_fields = [
            "first_name",
            "last_name",
            "years_of_experience",
            "email"
        ]

        response = self.client.get(url)

        for field in additional_fields:
            self.assertContains(response, field)

    def test_cook_filter_by_experience_title(self):
        url = reverse("admin:kitchen_cook_changelist")

        response = self.client.get(url)

        self.assertContains(response, "By experience")

    def test_cook_filter_by_experience_contains_custom_lookups(self):
        url = reverse("admin:kitchen_cook_changelist")

        response = self.client.get(url)

        self.assertContains(response, "less than 5 years")
        self.assertContains(response, "5-10 years")
        self.assertContains(response, "10-15 years")
        self.assertContains(response, "20+ years")

    def test_cook_filter_by_experience_works_correctly(self):
        url = reverse("admin:kitchen_cook_changelist") + "?year=15"

        response = self.client.get(url)

        self.assertContains(response, "ava.davis@email.com")
        self.assertContains(response, "olly2000")

    def test_cook_years_of_experience_field_on_edit_page(self):
        url = reverse("admin:kitchen_cook_change", args=[self.admin_user.pk])

        response = self.client.get(url)

        self.assertContains(response, "years_of_experience")

    def test_dish_search_field_only_on_dish_list_page_and_works(self):
        url = reverse("admin:kitchen_dish_changelist") + "?q=borsch"

        response = self.client.get(url)

        self.assertContains(response, 'name="q"', count=1)
        self.assertContains(response, "Green Borscht")
        self.assertContains(response, "Vegetarian Borscht")
        self.assertNotContains(response, "Carbonara")
        self.assertNotContains(response, "Meat boom!")

    def test_dish_filter_by_dish_type_title(self):
        url = reverse("admin:kitchen_dish_changelist")

        response = self.client.get(url)

        self.assertContains(response, "By dish type")

    def test_dish_filter_by_dish_type_only_on_page_and_works(self):
        filter_ = "?type=12"
        url = reverse("admin:kitchen_dish_changelist") + filter_

        response = self.client.get(url)

        self.assertContains(response, filter_, count=1)
        self.assertContains(response, "Baked Carp")
        self.assertContains(response, "Grilled Black Sea Mussels")
        self.assertNotContains(response, "Green Borscht")
        self.assertNotContains(response, "Cabbage Rolls")
