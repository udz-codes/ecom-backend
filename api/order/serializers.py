from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user',
            'product_names',
            'total_products',
            'transaction_id',
            'total_amount',
            'address',
            'phone',
            'email'
        )