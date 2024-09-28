from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from kitchen.models import Cook, Dish, DishType
from kitchen.forms import (
    DishTypeNameSearchForm,
    DishNameSearchForm,
    DishForm,
    CookUsernameSearchForm,
    CookCreationForm,
    CookExperienceUpdateForm,
)


class CreateUpdateViewMixin:
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
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["create_url"] = reverse_lazy("kitchen:dish-type-create")
        context["search_form"] = DishTypeNameSearchForm(initial={"name": name})
        context["list_title"] = (
            f"{self.model._meta.verbose_name_plural.capitalize()} list"
        )
        return context

    def get_queryset(self):
        form = DishTypeNameSearchForm(self.request.GET)
        queryset = super().get_queryset()

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        else:
            print(form.errors)
        return queryset


class DishTypeCreateView(
    LoginRequiredMixin,
    CreateUpdateViewMixin,
    generic.CreateView
):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(
    LoginRequiredMixin,
    CreateUpdateViewMixin,
    generic.UpdateView
):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["create_url"] = reverse_lazy("kitchen:dish-create")
        context["search_form"] = DishNameSearchForm(initial={"name": name})
        context["list_title"] = (
            f"{self.model._meta.verbose_name_plural.capitalize()} list"
        )
        return context

    def get_queryset(self):
        form = DishNameSearchForm(self.request.GET)
        queryset = super().get_queryset().select_related("dish_type")

        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                return queryset.filter(name__icontains=name)

        return queryset


class DishCreateView(
    LoginRequiredMixin,
    CreateUpdateViewMixin,
    generic.CreateView
):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = (
        Dish.objects.
        select_related("dish_type").
        prefetch_related("cooks")
    )

    def post(self, request, *args, **kwargs):
        dish = self.get_object()

        if dish.cooks.filter(id=request.user.id).exists():
            dish.cooks.remove(request.user)
        else:
            dish.cooks.add(request.user)

        return HttpResponseRedirect(
            reverse_lazy("kitchen:dish-detail", args=[dish.id])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_object().cooks.filter(id=self.request.user.id).exists():
            context["change_status"] = "Delete me from this dish"
            context["button_class"] = "btn btn-danger"
        else:
            context["change_status"] = "Assign me to this dish"
            context["button_class"] = "btn btn-success"

        return context


class DishUpdateView(
    LoginRequiredMixin,
    CreateUpdateViewMixin,
    generic.UpdateView
):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["create_url"] = reverse_lazy("kitchen:cook-create")
        context["search_form"] = CookUsernameSearchForm(
            initial={"username": username}
        )
        context["list_title"] = (
            f"{self.model._meta.verbose_name_plural.capitalize()} list"
        )
        return context

    def get_queryset(self):
        form = CookUsernameSearchForm(self.request.GET)
        queryset = super().get_queryset().prefetch_related("dishes")

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class CookCreateView(
    LoginRequiredMixin,
    CreateUpdateViewMixin,
    generic.CreateView
):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = get_user_model().objects.prefetch_related("dishes__dish_type")


class CookExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")
