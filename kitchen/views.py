from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    DishTypeNameSearchForm,
    DishNameSearchForm,
    DishForm,
    CookLastNameSearchForm,
    CookCreationForm,
    CookExperienceUpdateForm,
)
from .models import Cook, Dish, DishType


class BaseCreateUpdateView(LoginRequiredMixin):
    template_name = "kitchen/create_update_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model._meta.verbose_name
        object_name = self.object

        if model_name == "cook":
            object_name = "years of experience"

        context["title"] = (
            f"Update {object_name}" if self.object else f"Create {model_name}"
        )
        return context

    class Meta:
        abstract = True


class BaseDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "kitchen/confirm_delete.html"

    class Meta:
        abstract = True


@login_required
def index(request):
    context = {
        "num_cooks": Cook.objects.count(),
        "num_dishes": Dish.objects.count(),
        "num_dish_types": DishType.objects.count(),
    }

    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = DishTypeNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = DishTypeNameSearchForm(self.request.GET)
        self.queryset = DishType.objects.all()

        if form.is_valid():
            return self.queryset.filter(
                name__startswith=form.cleaned_data["name"]
            )

        return self.queryset


class DishTypeCreateView(BaseCreateUpdateView, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(BaseCreateUpdateView, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(BaseDeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = DishNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = DishNameSearchForm(self.request.GET)
        self.queryset = Dish.objects.select_related("dish_type")

        if form.is_valid():
            return self.queryset.filter(
                name__startswith=form.cleaned_data["name"]
            )

        return self.queryset


class DishCreateView(BaseCreateUpdateView, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related(
        "dish_type"
    ).prefetch_related(
        "cooks"
    )


class DishUpdateView(BaseCreateUpdateView, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(BaseDeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")

        context["search_form"] = CookLastNameSearchForm(
            initial={"last_name": last_name}
        )
        return context

    def get_queryset(self):
        form = CookLastNameSearchForm(self.request.GET)
        self.queryset = get_user_model().objects.prefetch_related("dishes")

        if form.is_valid():
            return self.queryset.filter(
                last_name__startswith=form.cleaned_data["last_name"]
            )

        return self.queryset


class CookCreateView(BaseCreateUpdateView, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = get_user_model().objects.prefetch_related("dishes__dish_type")


class CookExperienceUpdateView(BaseCreateUpdateView, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(BaseDeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = get_user_model().objects.get(id=request.user.id)
    if Dish.objects.get(id=pk) in cook.dishes.all():
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
