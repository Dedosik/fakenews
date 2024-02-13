from django.urls import path

from checks import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('archive/', views.ChecksArchive.as_view(), name='archive'),
    path('my-pdf/', views.my_pdf, name='my-checks-pdf'),
    path('pdf-users/', views.users_pdf, name='users-checks-pdf'),
]
