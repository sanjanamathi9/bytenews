from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path
from . import views
app_name = 'news'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # App URL includes# ✅ Include once with namespace
    path('users/', include('users.urls')),              # User-related URLs
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),

    
    # Optional: logged out message page
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html')),
]


