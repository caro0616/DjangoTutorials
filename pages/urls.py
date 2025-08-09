from django.urls import path
from .views import HomePageView, AboutPageView, ProductIndexView, ProductShowView, ProductCreateView , CartView, CartRemoveAllView

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("products/", ProductIndexView.as_view(), name='product_index'),
    path("products/create/", ProductCreateView.as_view(), name='product_create'),
    path("products/<str:id>/", ProductShowView.as_view(), name='product_show'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>/', CartView.as_view(), name='cart_add'),
    path('cart/removeAll/', CartRemoveAllView.as_view(), name='cart_removeAll'),
    
    
]
