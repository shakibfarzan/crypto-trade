from decimal import Decimal
from django.db import models

class Historical(models.Model):
    name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=20, decimal_places=3, default=Decimal('0.0'))
    volume = models.DecimalField(max_digits=20, decimal_places=3, default=Decimal('0.0'))
    dominance = models.DecimalField(max_digits=20, decimal_places=3, default=Decimal('0.0'))
    created_at = models.DateTimeField(auto_now_add=True)