from .views import *
from rest_framework import routers
from django.urls import path, include

from avito_app.views import (CategoryListAPIview, CategoryDetailAPIview,   UserProfileListAPIview, UserProfileUpdateSerializer,
                             SubCategoryListAPIview,SubCategoryDetailAPIview, ProductDetailAPIview, ProductListAPIview,  ReviewViewSet,
                             RegisterView, CustomLoginView, LogoutView)

router = routers.DefaultRouter()
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIview.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIview.as_view(), name='product_detail'),
    path('category/', CategoryListAPIview.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIview.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIview.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIview.as_view(), name='subcategory_detail'),
    path('user/', UserProfileListAPIview.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileUpdateAPIview.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', CustomLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('cart/', CartAPIView.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorite/', FavoriteAPIView.as_view(), name='favorite_detail'),
    path('favorite_item/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('favorite_item/<int:pk>', FavoriteItemViewSet.as_view({'delete': 'destroy'}))
]