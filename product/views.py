from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
    ReviewDetailSerializer,
)


@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()

    list_ = CategorySerializer(categories, many=True).data

    return Response(data=list_)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(
            data={'error': 'category not found!'},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = CategoryDetailSerializer(category, many=False).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()

    list_ = ProductSerializer(products, many=True).data

    return Response(data=list_)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data={'error': 'product not found!'},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = ProductDetailSerializer(product, many=False).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()

    list_ = ReviewSerializer(reviews, many=True).data

    return Response(data=list_)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            data={'error': 'review not found!'},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = ReviewDetailSerializer(review, many=False).data

    return Response(data=data, status=status.HTTP_200_OK)
@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()

    data = []

    for product in products:
        reviews = Review.objects.filter(product=product)

        product_data = ProductSerializer(product).data

        product_data['reviews'] = ReviewSerializer(
            reviews, many=True
        ).data

        product_data['rating'] = reviews.aggregate(
            Avg('stars')
        )['stars__avg']

        data.append(product_data)

    return Response(data=data)