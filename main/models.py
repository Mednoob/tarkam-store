import uuid
from django.db import models

class Product(models.Model):
    CATEGORIES = [
        # Will add later
        ("other", "Other")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
