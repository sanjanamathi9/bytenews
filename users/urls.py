from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register
app_name = 'users' 
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('preferences/', views.preferences, name='preferences'),
]