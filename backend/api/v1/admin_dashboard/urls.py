from django.urls import path

from . import views

urlpatterns = [
    # CATEGORIES
    path('categories/', views.CategoryViewSet.as_view({'get': 'list'}), name = "list"),
    path('category/add/', views.CategoryViewSet.as_view({'post': 'create'}), name = "add"),
    path('category/edit_and_detail/<str:slug>/', views.CategoryViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name = "edit_detail"),
    path('category/destroy/<str:slug>/', views.CategoryViewSet.as_view({'delete': 'destroy'}), name = "destroy"),
    # END CATEGORIES
    # PRODUCT
    path('products/', views.ProductViewSet.as_view({'get': 'list'}), name = 'product_list'),
    path('product/add/', views.ProductViewSet.as_view({'post': 'create'}), name = 'product_add'),
    path('product/edit_and_detail/<str:slug>/', views.ProductViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name = 'product_edit_detail'),
    path('product/destroy/<str:slug>/', views.ProductViewSet.as_view({'delete': 'destroy'}), name = 'product_destroy'),
    # END PRODUCT

    path('reviews/', views.ReviewAPiView.as_view({'get': 'list'}), name = "review_list"),
    
]