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
    path("scratch/", views.scratch_page, name="scratch"),
    path("save-design/", views.save_design_ajax, name="save_design_ajax"),
    path('configure/', views.configure_sign, name='configure_sign'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout_page'),
    path('secure-checkout/', views.final_checkout, name='secure_checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
]