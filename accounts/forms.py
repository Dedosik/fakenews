from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {"username": "Логин:", "first_name": "Имя:", "last_name": "Фамилия:", "email": "Email:"}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин ")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {"username": "Логин:", "first_name": "Имя:", "last_name": "Фамилия:", "email": "Email:"}

    def __init__(self, *args, user=None, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.user = user

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username__iexact=username)

        if users:
            if self.user:
                if self.user.username != username:
                    raise forms.ValidationError("Такой логин занят")
            else:
                raise forms.ValidationError("Такой логин занят")

        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("middle_name", "subscribed", "free_checks")
        labels = {"middle_name": "Отчество:", "subscribed": "Подписка:", "free_checks": "Беслпатные проверки:"}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserCreateForm(UserForm):

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
