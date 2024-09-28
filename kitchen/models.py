from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from restaurant_kitchen_service.settings import AUTH_USER_MODEL


class Cook(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    years_of_experience = models.IntegerField(
        default=0,
        verbose_name="years of experience",
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )

    class Meta:
        ordering = (Lower("username"),)

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return f'"{self.username}"'


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = (Lower("name"),)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().capitalize()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'dish type: "{self.name}"'


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().capitalize()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "dishes"
        ordering = (Lower("name"),)
        default_related_name = "dishes"
        indexes = [models.Index(fields=["price"])]

    def __str__(self) -> str:
        return f'dish: "{self.name}"'
