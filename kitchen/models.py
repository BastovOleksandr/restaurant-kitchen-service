from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.core.validators import MinValueValidator, MaxValueValidator


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(
        default=0,
        verbose_name="years of experience",
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )

    class Meta:
        verbose_name = "Cook"
        verbose_name_plural = "Cooks"
        ordering = (Lower("username"),)
        indexes = [models.Index(fields=["username"])]

    def __str__(self) -> str:
        return (
            f'Username: "{self.username}"\n'
            f'First name: "{self.first_name}"\n'
            f'Last name: "{self.last_name}"'
            f'Experience: "{self.years_of_experience}" years'
        )


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Dish type"
        verbose_name_plural = "Dish types"
        ordering = (Lower("name"),)
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return f'Dish type: "{self.name}"'


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(get_user_model())

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        ordering = (Lower("name"),)
        default_related_name = "dishes"
        indexes = [
            models.Index(fields=["name"]), models.Index(fields=["price"])
        ]

    def __str__(self) -> str:
        return (
            f'Dish name: "{self.name}"\n'
            f'Type: "{self.dish_type.name}"\n'
            f'Price: "{self.price}"'
        )
