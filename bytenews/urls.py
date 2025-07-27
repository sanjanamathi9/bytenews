from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from news.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    # ✅ Home page goes to landing page
    path('', landing_page, name='landing'),

    # ✅ Article list at /articles/
    path('articles/', include('news.urls')),
    

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html')),
    path('admin/', admin.site.urls),
    # News app with namespace
    
]
