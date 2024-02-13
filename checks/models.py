from django.contrib.auth.models import User
from django.db import models


class News(models.Model):

    user = models.ForeignKey(User, related_name="news", on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_fake = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    @classmethod
    def get_stats(cls):
        news = cls.objects.all()
        all_count = news.count()
        fake = news.filter(is_fake=True).count()
        not_fake = news.filter(is_fake=False).count()
        return {
            "all": all_count,
            "fake": fake,
            "not_fake": not_fake,
            "undefined": all_count - fake - not_fake
        }
