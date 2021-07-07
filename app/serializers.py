from django.contrib.auth.hashers import make_password
from rest_framework import serializers, reverse
from .models import *

class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    user_detail_url = serializers.SerializerMethodField()

    def get_user_detail_url(self, user):
        return reverse.reverse(viewname='user-detail', request=self.context['request'], args=(user.pk,))

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'tel', 'user_detail_url']

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    date_joined = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def update(self, instance, validated_data):
        if 'password' in validated_data.keys():
            validated_data['password'] = make_password(validated_data['password'])
        if 'headshot' in validated_data.keys() and instance.headshot.name != 'default_user_headshot.jpeg':
            instance.headshot.delete(True)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'tel', 'first_name', 'last_name', 'headshot', 'address', 'date_joined']

class CategoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    goods_num = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    goods_list_url = serializers.SerializerMethodField()

    def get_goods_list_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            if obj.id is None:
                obj.id = Category.objects.get(name=obj.name).id
            return reverse.reverse(viewname='goods-list', request=request, args=(obj.id, ))

    def get_goods_num(self, obj):
        goods_num = Goods.objects.filter(category_id=obj.id).count()
        for category_obj in Category.objects.filter(parent=obj.id):
            goods_num += self.get_goods_num(category_obj)
        return goods_num

    def get_id(self, obj):
        return Category.objects.get(name=obj.name).id

    def get_sub_categories(self, obj):
        try:
            meta = self.context['request'].META
            scheme = meta['wsgi.url_scheme']
            http_host = meta['HTTP_HOST']
            uri = '%s://%s' % (scheme, http_host)
        except:
            uri = ''
        finally:
            return self._get_sub_categories(uri, obj)

    def _get_sub_categories(self, uri, obj):
        categories = []
        queryset = Category.objects.filter(parent=obj.id)
        for category_obj in queryset:
            category = dict(CategoryDetailSerializer(category_obj).data)
            category['headshot'] = uri + category['headshot']
            category['goods_list_url'] = self.get_goods_list_url(category_obj)
            category['goods_num'] = self.get_goods_num(category_obj)
            category['sub_categories'] = self._get_sub_categories(uri, category_obj)
            categories.append(category)
        return categories

    class Meta:
        model = Category
        fields = ['id', 'name', 'headshot', 'parent', 'goods_num', 'goods_list_url', 'sub_categories']

class CategoryListSerializer(CategoryDetailSerializer):
    category_detail_url = serializers.SerializerMethodField()

    def get_category_detail_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            if obj.id is None:
                obj.id = Category.objects.get(name=obj.name).id
            return reverse.reverse(viewname='category-detail', request=request, args=(obj.id, ))

    def _get_sub_categories(self, uri, obj):
        categories = []
        queryset = Category.objects.filter(parent=obj.id)
        for category_obj in queryset:
            category = dict(CategoryDetailSerializer(category_obj).data)
            category['headshot'] = uri + category['headshot']
            category['goods_num'] = self.get_goods_num(category_obj)
            category['category_detail_url'] = self.get_category_detail_url(category_obj)
            category['goods_list_url'] = self.get_goods_list_url(category_obj)
            category['sub_categories'] = self._get_sub_categories(uri, category_obj)
            categories.append(category)
        return categories

    class Meta:
        model = Category
        fields = ['id', 'name', 'headshot', 'parent', 'goods_num', 'category_detail_url', 'goods_list_url', 'sub_categories']

class GoodsListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    goods_detail_url = serializers.SerializerMethodField()

    def get_category(self, obj):
        kwargs = self.context['view'].kwargs
        category_id = kwargs['category_id']
        return Category.objects.get(id=category_id).name

    def get_id(self, goods):
        return Goods.objects.get(name=goods.name).id

    def get_goods_detail_url(self, goods):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            if goods.id is None:
                goods.id = Goods.objects.get(name=goods.name).id
            return reverse.reverse(viewname='goods-detail', request=request,
                                   args=(goods.category.id, goods.id))

    def create(self, validated_data):
        kwargs = self.context['view'].kwargs
        category_id = kwargs['category_id']
        validated_data['category_id'] = category_id
        return super().create(validated_data)

    class Meta:
        model = Goods
        fields = ['id', 'name', 'unit_price', 'stock', 'category', 'headshot', 'goods_detail_url']

class GoodsDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category = serializers.SerializerMethodField()
    goods_image_list_url = serializers.SerializerMethodField()
    goods_video_list_url = serializers.SerializerMethodField()

    def get_category(self, obj):
        kwargs = self.context['view'].kwargs
        category_id = kwargs['category_id']
        return Category.objects.get(id=category_id).name

    def get_goods_image_list_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            return reverse.reverse(viewname='goods-image-list', request=request, args=(obj.category.id, obj.id))

    def get_goods_video_list_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            return reverse.reverse(viewname='goods-video-list', request=request, args=(obj.category.id, obj.id))

    class Meta:
        model = Goods
        fields = ['id', 'name', 'unit_price', 'stock', 'category', 'headshot', 'goods_image_list_url', 'goods_video_list_url']

class GoodsImageListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    # goods_id = serializers.ReadOnlyField()
    # category_id = serializers.ReadOnlyField()

    goods_image_detail_url = serializers.SerializerMethodField()

    def get_id(self, obj):
        return GoodsImage.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id

    def get_goods_image_detail_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            if obj.id is None:
                obj.id = GoodsImage.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id
            return reverse.reverse(viewname='goods-image-detail', request=request,
                                   args=(obj.goods.category_id, obj.goods_id, obj.id))

    def create(self, validated_data):
        kwargs = self.context['view'].kwargs
        goods_id = kwargs['goods_id']
        category_id = kwargs['category_id']
        validated_data['goods_id'] = goods_id
        validated_data['category_id'] = category_id
        return super().create(validated_data)

    class Meta:
        model = GoodsImage
        fields = ['id', 'file_name', 'created', 'title', 'goods_image_detail_url']

class GoodsImageDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    # goods_id = serializers.ReadOnlyField()
    # category_id = serializers.ReadOnlyField()

    def get_id(self, obj):
        return GoodsImage.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id

    def create(self, validated_data):
        kwargs = self.context['view'].kwargs
        goods_id = kwargs['goods_id']
        category_id = kwargs['category_id']
        validated_data['goods_id'] = goods_id
        validated_data['category_id'] = category_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'file_name' in validated_data.keys():
            instance.file_name.delete(True)
        return super().update(instance, validated_data)

    class Meta:
        model = GoodsImage
        fields = ['id', 'file_name', 'created', 'title']

class GoodsVideoListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    # goods_id = serializers.ReadOnlyField()
    # category_id = serializers.ReadOnlyField()

    goods_video_detail_url = serializers.SerializerMethodField()

    def get_id(self, obj):
        return GoodsVideo.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id

    def get_goods_video_detail_url(self, obj):
        try:
            request = self.context['request']
        except:
            request = None
        finally:
            if obj.id is None:
                obj.id = GoodsVideo.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id
            return reverse.reverse(viewname='goods-video-detail', request=request,
                                   args=(obj.goods.category_id, obj.goods_id, obj.id))

    def create(self, validated_data):
        kwargs = self.context['view'].kwargs
        goods_id = kwargs['goods_id']
        category_id = kwargs['category_id']
        validated_data['goods_id'] = goods_id
        validated_data['category_id'] = category_id
        return super().create(validated_data)

    class Meta:
        model = GoodsVideo
        fields = ['id', 'file_name', 'created', 'title', 'goods_video_detail_url']

class GoodsVideoDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    # goods_id = serializers.ReadOnlyField()
    # category_id = serializers.ReadOnlyField()

    def get_id(self, obj):
        return GoodsVideo.objects.get(title=obj.title, category=obj.category, goods=obj.goods).id

    def create(self, validated_data):
        kwargs = self.context['view'].kwargs
        goods_id = kwargs['goods_id']
        category_id = kwargs['category_id']
        validated_data['goods_id'] = goods_id
        validated_data['category_id'] = category_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'file_name' in validated_data.keys():
            instance.file_name.delete(True)
        return super().update(instance, validated_data)

    class Meta:
        model = GoodsVideo
        fields = ['id', 'file_name', 'created', 'title']