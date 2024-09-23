from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, Cook, DishType


class BaseSearchByNameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["name"].label = ""
        self.fields["name"].widget.attrs.update(
            {
                "max_length": self.fields["name"].max_length,
                "placeholder": "Search by name",
            }
        )


class DishNameSearchForm(BaseSearchByNameForm):
    class Meta:
        model = Dish
        fields = ["name"]


class DishTypeNameSearchForm(BaseSearchByNameForm):
    class Meta:
        model = DishType
        fields = ["name"]


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]


class CookLastNameSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by last name"}),
    )
