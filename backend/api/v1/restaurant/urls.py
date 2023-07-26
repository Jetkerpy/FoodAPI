from django.urls import path

from . import views

urlpatterns = [
    path('', views.restaurant, name = 'restaurant'),
    path('addresses/', views.addresses, name = 'addresses'),
    path('post_feedback/', views.post_feedback, name = 'post_feedback'),
    
]