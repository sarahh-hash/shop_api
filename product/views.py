from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from django.db.models import Avg

from .models import Category, Product, Review

from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    CategoryValidateSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
    ReviewDetailSerializer,
)


class TotalPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = TotalPagination

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field ='id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryDetailSerializer
        return CategorySerializer
class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = TotalPagination

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductSerializer

class ReviewListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = TotalPagination

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = ReviewSerializer
    lookup_field ='id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewDetailSerializer
        return ProductSerializer


class ProductReviewsAPIView(APIView):

    def get(self, request):
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