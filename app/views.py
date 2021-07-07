from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import (UserListSerializer, UserDetailSerializer, CategoryListSerializer,
                          CategoryDetailSerializer, GoodsListSerializer, GoodsDetailSerializer,
                          GoodsImageListSerializer, GoodsImageDetailSerializer, GoodsVideoListSerializer,
                          GoodsVideoDetailSerializer)
from .models import User, Category, Goods, GoodsVideo, GoodsImage
from .permissions import IsUserSelfOrReadonly, IsAdminOrReadonly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format)
    })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserSelfOrReadonly]

class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

    def get(self, request, *args, **kwargs):
        self.queryset = Category.objects.filter(parent=0)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.queryset = Category.objects.all()
        return super().post(request, *args, **kwargs)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

class GoodsList(generics.ListCreateAPIView):
    serializer_class = GoodsListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

    def get_subcategory_ids(self, category_id):
        ids = []
        queryset = Category.objects.filter(parent=category_id)
        for category_obj in queryset:
            ids.append(category_obj.id)
            ids += self.get_subcategory_ids(category_obj.id)

        return ids

    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        ids = self.get_subcategory_ids(category_id)
        ids.append(category_id)
        self.queryset = Goods.objects.filter(category__in=ids)
        return super().get(request, *args, **kwargs)

class GoodsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoodsDetailSerializer
    queryset = Goods.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

class GoodsImageList(generics.ListCreateAPIView):
    serializer_class = GoodsImageListSerializer
    queryset = GoodsImage.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

class GoodsImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoodsImageDetailSerializer
    queryset = GoodsImage.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

class GoodsVideoList(generics.ListCreateAPIView):
    serializer_class = GoodsVideoListSerializer
    queryset = GoodsVideo.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]

class GoodsVideoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoodsVideoDetailSerializer
    queryset = GoodsVideo.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadonly]