from django.core.management import call_command
from django.core.validators import MaxValueValidator, MinValueValidator
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class CookModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def setUp(self):
        self.cook = get_user_model().objects.get(id=1)

    def test_str(self):
        self.assertEqual(str(self.cook), f'"{self.cook.username}"')

    def test_get_absolute_url_should_return_correct_url(self):
        self.assertEqual(
            self.cook.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": self.cook.pk}),
        )

    def test_years_of_experience_field_max_min_values(self):
        field = self.cook._meta.get_field("years_of_experience")
        validators = field.validators
        max_value = next(
            v.limit_value
            for v in validators if isinstance(v, MaxValueValidator)
        )
        min_value = next(
            v.limit_value
            for v in validators if isinstance(v, MinValueValidator)
        )

        self.assertEqual(max_value, 50)
        self.assertEqual(min_value, 0)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.cook.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": self.cook.pk}),
        )
