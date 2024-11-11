from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.all_products, name='products'),
    path('lashes/', views.lashes, name='lashes'), 
    path('glue/', views.glue, name='glue'),
    path('other/', views.other, name='other'), 
    path('contact/', views.contact, name='contact'),

    # Search
    path('search/', views.product_search, name='product_search'),

    # Products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('glue/<int:product_id>/', views.glue_detail, name='glue_detail'),
    path('other/<int:product_id>/', views.other_detail, name='other_detail'), 
    path('special-offers/', views.special_offers, name='special_offers'),

    # Other Paths
    path('admin/products/', views.admin_product_view, name='admin_product_view'),
    path('manager/', views.manager_view, name='manager_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
