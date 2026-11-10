from django.urls import path
from . import views

urlpatterns = [
    # Категории
    path('categories/', views.category_list_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),

    # Товары
    path('products/', views.product_list_api_view),
    path('products/<int:id>/', views.product_detail_api_view),

    # Отзывы
    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),

    # Товары с отзывами и рейтингом
    path('products/reviews/', views.product_reviews_api_view),
]