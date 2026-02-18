from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path("",index,name="index"),
    path('products/', views.all_products, name='all_products'), # The landing page
    path('products/<str:product_slug>/', views.product_detail, name='product_detail'),
    path('services/', views.services, name='services'),
    path('materials/', views.material, name='materials'),
    path('contact/', views.contact, name='contact'),
]