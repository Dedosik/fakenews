from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


class RegistrationView(View):

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()

            return redirect(reverse("login"))

        return redirect(reverse("registration"))

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, "accounts/registration.html", {"form": form})


class LoginView(View):

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is None:
                messages.warning(request, "Неверный логин или пароль")
                return redirect(reverse("login"))

            if not user.is_active:
                return HttpResponse("Disabled account")

            login(request, user)
            return redirect((reverse("index")))

        return render(request, "accounts/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_form = UserForm(instance=user, data=request.POST, user=user)
        profile_form = ProfileForm(instance=user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль изменен")

            return redirect(reverse("profile"))

        if user_form.errors.get("username"):
            messages.warning(request, user_form.errors.get("username"))
        messages.warning(request, "Форма заполнена некорректно")
        return redirect(reverse("profile"))

    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        stats = user.profile.get_checks_stats()
        return render(request, "accounts/profile.html", {
            "user_form": user_form,
            "profile_form": profile_form,
            "stats": stats
        })


class SubscriptionsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, "accounts/subscribes.html", {})


def subscribe(request):
    user = request.user
    if user.profile.subscribed:
        return HttpResponse("Вы уже подписаны!")
    user.profile.subscribed = True
    user.profile.save()
    return HttpResponse("Подписка оформлена!")
