import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORIES = [
        ("shoes", "Shoes"),
        ("clothes", "Clothes"),
        ("accessories", "Accessories"),
        ("balls", "Balls"),
        ("other", "Other")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
