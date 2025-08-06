from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from news.views import landing_page, ArticleViewSet, UserPreferenceViewSet  # ✅ Added UserPreferenceViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers  # ✅ Imported DRF router
from news.views import ArticleViewSet, UserPreferenceViewSet
from news.views import CategoryViewSet  # ✅ Ensure this import exists
from news.views import GenerateAudioAPIView

# ✅ Set up DRF router for API
router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)  # Expose /api/articles/
router.register(r'preferences', UserPreferenceViewSet, basename='userpreference')  # ✅ FIXED: added basename
router.register(r'categories', CategoryViewSet)  # Expose /api/categories/

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

    # ✅ API endpoint base URL
    path('api/', include(router.urls)),

    path('', include('news.urls')),  # ✅ Keep news app routes
    path('users/', include('users.urls')),  # ✅ Keep user app routes
    path('api/', include(router.urls)),  # Keep this!
    path('api/articles/<int:pk>/generate_audio/', GenerateAudioAPIView.as_view(), name='api_generate_audio'),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
