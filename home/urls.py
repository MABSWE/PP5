from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import subscribe

urlpatterns = [
    path('', views.index, name='home'),
    path('subscribe/', views.subscribe_to_newsletter, name='subscribe'),
    path("subscribe/", subscribe, name="subscribe"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
