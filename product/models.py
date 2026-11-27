from django.db import models

from django.db.models import CASCADE

from users.models import CustomUser
from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(BaseModel):
    text = models.TextField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    stars = models.IntegerField(choices=[
            (1, '1 звезда'),
            (2, '2 звезды'),
            (3, '3 звезды'),
            (4, '4 звезды'),
            (5, '5 звёзд'),
        ],
        default=5)

    def __str__(self):
        return self.text[:50]