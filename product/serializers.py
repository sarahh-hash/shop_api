from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return Product.objects.filter(category=obj).count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return Product.objects.filter(category=obj).count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_rating(self, obj):
        return obj.reviews.aggregate(
            rating=Avg('stars')
        )['rating']




class CategoryValidateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        error_messages={
            'blank': 'Название категории не должно быть пустым!',
            'required': 'Необходимо указать название категории!'
        }
    )

    class Meta:
        model = Category
        fields = ['name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Название не должно быть пустым!'
            )
        return value


class ProductValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Название продукта не должно быть пустым!'
            )
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Описание продукта не должно быть пустым!'
            )
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Цена продукта не должна быть отрицательной!'
            )
        return value

class ReviewValidateSerializer(serializers.ModelSerializer):

    text = serializers.CharField(
        error_messages={
            'blank': 'Текст отзыва не должен быть пустым!',
            'required': 'Необходимо написать текст отзыва!'
        }
    )

    stars = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ['text', 'product', 'stars']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Текст отзыва не должен быть пустым!'
            )
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 5!'
            )
        return value