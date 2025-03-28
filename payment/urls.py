from django.urls import path
from payment import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name="billing_info"),
    path('process_order/', views.process_order, name="process_order")

]