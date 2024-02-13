from django.urls import path

from stats import views

urlpatterns = [
    path('users/', views.UsersListView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='users-create'),
    path('users/edit/<int:uid>/', views.UserEditView.as_view(), name='users-edit'),
    path('users/delete/<pk>/', views.UserDeleteView.as_view(), name='users-delete'),
    path('checks/', views.ChecksListView.as_view(), name='checks'),
    path("checks/<pk>/", views.CheckDetailsView.as_view(), name="checks-details"),
    path('checks/delete/<pk>/', views.CheckDeleteView.as_view(), name='checks-delete'),
    path('', views.StatsView.as_view(), name='stats'),
]
