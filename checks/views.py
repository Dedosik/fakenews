from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView

from .business import check
from .business.geneate_pdf import generate_pdf
from .forms import NewsForm
from .models import News


class IndexView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile
        if not profile.has_access():
            messages.warning(
                request,
                f"У вас закончились попытки. Оформите <a href={reverse_lazy('subscriptions')}>подписку</a>"
            )
            return redirect(reverse("index"))
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user
            news.save()
            predict = check.is_fake(news.title)
            news.is_fake = bool(predict)
            news.save()

            messages.success(request, f"Новость проверена: {'Фейк' if predict else 'Не фейк' }")
            profile.do_check()
            return redirect(reverse("index"))

        messages.warning(request, "Форма заполнена неправильно")
        return redirect(reverse("index"))

    def get(self, request, *args, **kwargs):
        form = NewsForm()
        accuracy = check.accuracy * 100
        return render(request, "checks/index.html", {"form": form, "accuracy": accuracy})


class ChecksArchive(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = News
    context_object_name = "objects"
    template_name = "checks/archive.html"
    ordering = ["-created"]

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=u)


@login_required
def my_pdf(request):

    user = request.user
    news = News.objects.filter(user=user)
    pdf = generate_pdf(news)

    return FileResponse(pdf, as_attachment=True, filename=f"{user.username}-checks.pdf")


@login_required
def users_pdf(request, *args, **kwargs):
    if request.GET.get("user"):
        user = User.objects.filter(id=request.GET.get("user")).first()
        if not user:
            messages.warning(
                request,
                f"Такого пользователя не существует"
            )
            return redirect("index")
        news = News.objects.filter(user=user)
        filename = f"{user.username}-checks.pdf"
    else:
        news = News.objects.all()
        filename = "users-checks.pdf"

    pdf = generate_pdf(news)

    return FileResponse(pdf, as_attachment=True, filename=filename)
