from django import forms
from .models import News


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ("title", "body")
        labels = {"title": "Название", "body": "Содержание"}

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
