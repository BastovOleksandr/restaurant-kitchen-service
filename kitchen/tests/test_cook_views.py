from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

LIST_URL = reverse("kitchen:cook-list")
CREATE_URL = reverse("kitchen:cook-create")
EXPERIENCE_UPDATE_URL = reverse("kitchen:cook-update", kwargs={"pk": 1})
DELETE_URL = reverse("kitchen:cook-delete", kwargs={"pk": 1})
DETAIL_URL = reverse("kitchen:cook-detail", kwargs={"pk": 1})


class PublicCookViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "tests_kitchen_fixture.json")

    def test_list_view_login_required_and_redirect(self):
        response = self.client.get(LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={LIST_URL}')

    def test_create_view_login_required_and_redirect(self):
        response = self.client.get(CREATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={CREATE_URL}')

    def test_experience_update_view_login_required_and_redirect(self):
        response = self.client.get(EXPERIENCE_UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f'{reverse("login")}?next={EXPERIENCE_UPDATE_URL}'
        )

    def test_delete_view_login_required_and_redirect(self):
        response = self.client.get(DELETE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={DELETE_URL}')


class PrivateCookViewsTests(TestCase):
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
        self.assertEqual(len(response.context.get("cook_list")), 5)

    def test_list_view_correct_num_of_entries_on_next_page(self):
        response = self.client.get(LIST_URL + "?page=3")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("cook_list")), 4)

    def test_list_view_context_contain_search_by_username_and_it_works(self):
        response = self.client.get(LIST_URL + "?username=eNt")
        cooks_ = list(response.context.get("cook_list").values("username"))

        self.assertIn("search_form", response.context)
        self.assertTrue(len(cooks_) == 2)
        self.assertCountEqual(
            [{"username": "Adm1n_Entry"}, {"username": "UsEr_enTrY"}], cooks_
        )

    def test_create_view(self):
        data = {
            "username": "wwwlast_user",
            "first_name": "custom_first_name",
            "last_name": "custom_last_name",
            "password1": "123_aaaBB",
            "password2": "123_aaaBB",
            "email": "custom@email.com",
            "years_of_experience": 20,
        }

        response = self.client.post(CREATE_URL, data)
        custom_cook = get_user_model().objects.last()

        self.assertRedirects(
            response,
            reverse("kitchen:cook-detail", kwargs={"pk": custom_cook.pk})
        )
        self.assertTrue(
            get_user_model().objects.filter(username="wwwlast_user").exists()
        )

    def test_years_of_experience_update_view(self):
        data = {
            "years_of_experience": 14,
        }
        before = get_user_model().objects.get(pk=1)

        response = self.client.post(EXPERIENCE_UPDATE_URL, data)
        after = get_user_model().objects.get(pk=1)

        self.assertRedirects(response, LIST_URL)
        self.assertEqual(after.years_of_experience, 14)
        self.assertEqual(after.id, before.id)

    def test_delete_view(self):
        response = self.client.post(DELETE_URL)

        self.assertTrue(response.status_code == 302)
        self.assertEqual(response.url, LIST_URL)
        self.assertFalse(get_user_model().objects.filter(pk=1).exists())
