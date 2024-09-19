from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from kitchen.models import Cook, DishType, Dish
from kitchen import admin_filters

admin.site.unregister(Group)


@admin.register(Cook)
class CookAdmin(UserAdmin):
    search_fields = [
        "last_name",
    ]
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "years_of_experience",
        "is_staff",
        "is_superuser",
    )
    list_filter = [admin_filters.CookByYearsOfExperienceAdminFilter]
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "years_of_experience",
                )
            },
        ),
    )


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = [
        "name",
    ]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = [
        "name",
        "dish_type__name",
        "description",
        "price",
    ]
    list_filter = [
        admin_filters.DishByDishTypeAdminFilter,
    ]
