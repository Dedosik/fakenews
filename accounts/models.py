from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    subscribed = models.BooleanField(default=False)
    free_checks = models.IntegerField(default=5)

    def __str__(self):
        return f"Проифиль позователя {self.user}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def get_checks_stats(self):
        news = self.user.news.all()
        fake_news_count = news.filter(is_fake=True).count()
        return {
            "all": len(news),
            "fake": fake_news_count,
            "not_fake": len(news) - fake_news_count
        }

    def has_access(self):
        if not self.subscribed and self.free_checks < 1:
            return False
        return True

    def do_check(self):
        if not self.subscribed:
            self.free_checks -= 1
            self.save()

    @classmethod
    def get_stats(cls):
        profiles = cls.objects.all()
        all_count = profiles.count()
        subscribed = profiles.filter(subscribed=True).count()
        return {
            "all": all_count,
            "subscribed": subscribed,
            "not_subscribed": all_count - subscribed
        }


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
