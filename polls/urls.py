from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import  TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<str:game_slug>/', views.game_view, name='game_detail'),
    path('category/<str:category_slug>/', views.category_view, name='category_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    # path('change_item_quantity/', views.change_item_quantity_view, name='change_item_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/', views.order_create_view, name='order_create'),
    path('make_order/', views.make_order_view, name='make_order'),
    path('user_order/', views.user_orders_view, name='user_order'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('^thank_you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),

]

