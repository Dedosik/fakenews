from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DeleteView
from django.views.generic.detail import DetailView

from accounts.forms import UserCreateForm, UserForm, ProfileForm
from accounts.models import Profile
from checks.models import News
from .decorators import admin_only


@method_decorator(admin_only, name="dispatch")
class UsersListView(LoginRequiredMixin, ListView):

    model = User
    context_object_name = "users"
    template_name = "stats/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titles'] = ("ID", "Логин", "Email", "Имя", "Фамилия", "Отчество", "Бесплатные проверки", "Подписка")

        return context


@method_decorator(admin_only, name="dispatch")
class UserCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password = form.cleaned_data.get("password")
            new_user.save()

            messages.success(request, "Новый пользователь создан!")

            return redirect(reverse("users"))

        messages.warning(request, "Форма заполнена некорректно")
        return redirect(reverse("users-create"))

    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(
            request,
            "stats/create.html",
            {
                "page_title": "Создать пользователя",
                "form": form,
                "submit": "Создать",
            }
        )


@method_decorator(admin_only, name="dispatch")
class UserEditView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["uid"])
        user_form = UserForm(instance=user, data=request.POST, user=user)
        profile_form = ProfileForm(instance=user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Пользователь изменен!")

            return redirect(reverse("users-edit", kwargs=kwargs))

        messages.warning(request, "Форма заполнена некорректно")
        return redirect(reverse("users-edit", kwargs=kwargs))

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["uid"])
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        stats = user.profile.get_checks_stats()
        return render(
            request,
            "stats/edit-user.html",
            {
                "page_title": "Изменить пользователя",
                "user_form": user_form,
                "profile_form": profile_form,
                "submit": "Сохранить",
                "cur_user": user,
                "stats": stats,
            }
        )


@method_decorator(admin_only, name="dispatch")
class UserDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    success_url = reverse_lazy('users')
    template_name = 'stats/confirm.html'


@method_decorator(admin_only, name="dispatch")
class ChecksListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = News
    context_object_name = "checks"
    template_name = "stats/list-checks.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titles'] = ("ID", "Название", "Текст", "Создана", "Фейк", "Пользователь")

        return context


@method_decorator(admin_only, name="dispatch")
class CheckDetailsView(LoginRequiredMixin, DetailView):
    model = News
    template_name = "stats/details-check.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(admin_only, name="dispatch")
class CheckDeleteView(LoginRequiredMixin, DeleteView):

    model = News
    success_url = reverse_lazy('checks')
    template_name = 'stats/confirm.html'


@method_decorator(admin_only, name="dispatch")
class StatsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        news_stats = News.get_stats()
        subscriptions_stats = Profile.get_stats()
        return render(
            request,
            "stats/index.html",
            {
                "news_stats": news_stats,
                "subscriptions_stats": subscriptions_stats,
            }
        )
