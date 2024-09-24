from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from kitchen.models import DishType


class DishByDishTypeAdminFilter(admin.SimpleListFilter):
    title = _("dish type")
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return [(obj.pk, _(obj.name)) for obj in DishType.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dish_type=self.value())
        return queryset


class CookByYearsOfExperienceAdminFilter(admin.SimpleListFilter):
    title = _("experience")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        filter_ = {
            5: "less than 5",
            10: "5-10",
            15: "10-15",
            20: "20+",
        }
        return [
            (years, _(title + " years")) for years, title in filter_.items()
        ]

    def queryset(self, request, queryset):
        if self.value():
            year = int(self.value())
            return queryset.filter(
                years_of_experience__gte=year - 5,
            ).filter(
                years_of_experience__lte=year - 1
            )
        return queryset
