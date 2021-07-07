from django.urls import path
from .views import *

urlpatterns = [
    path('', api_root),

    path("categories/", CategoryList.as_view(), name='category-list'),
    path("categories/<int:id>/", CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:category_id>/goods/', GoodsList.as_view(), name='goods-list'),
    path('categories/<int:category_id>/goods/<int:id>/', GoodsDetail.as_view(), name='goods-detail'),

    path('categories/<int:category_id>/goods/<int:goods_id>/goods_images/',
         GoodsImageList.as_view(), name='goods-image-list'),
    path('categories/<int:category_id>/goods/<int:goods_id>/goods_videos/',
         GoodsVideoList.as_view(), name='goods-video-list'),
    path('categories/<int:category_id>/goods/<int:goods_id>/goods_images/<int:id>/',
         GoodsImageDetail.as_view(), name='goods-image-detail'),
    path('categories/<int:category_id>/goods/<int:goods_id>/goods_videos/<int:id>/',
         GoodsVideoDetail.as_view(), name='goods-video-detail'),

    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail')
]