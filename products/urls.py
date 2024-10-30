from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.all_products, name='products'),
    path('lashes/', views.lashes, name='lashes'), 
    path('glue/', views.glue, name='glue'),
    path('other/', views.other, name='other'), 
    path('contact/', views.contact, name='contact'), # Ny väg för kontakt
]