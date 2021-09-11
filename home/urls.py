from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-home'),
    path('login/', views.login, name='home-login'),
    path('offer/', views.offer, name='home-offer'),
    path('restaurants/', views.restaurants, name='home-restaurants'),
    path('south/', views.south, name='home-south'),
    path('pizza/', views.pizza, name='home-pizza'),
    path('burger/', views.burger, name='home-burger'),
    path('dessert/', views.dessert, name='home-dessert'),
    path('price/', views.price, name='filter-price'),
    path('rating/', views.rating, name='filter-rating'),
    path('cuisine/', views.cuisine, name='filter-cuisine'),
    path('about-us/', views.about, name='home-about'),
    path('faq/', views.faq, name='home-faq'),
    path('privacy-policy/', views.privacy_policy, name='home-privacy-policy'),
    path('terms-of-use/', views.terms_of_use, name='home-terms-of-use')
]