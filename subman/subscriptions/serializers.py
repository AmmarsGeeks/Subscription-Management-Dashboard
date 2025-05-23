from rest_framework import serializers
from .models import Subscription
from django.utils import timezone
import datetime

class DateOnlyField(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime.datetime):
            value = value.date()
        return super().to_representation(value)

class SubscriptionSerializer(serializers.ModelSerializer):
    monthly_cost = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    annual_cost = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    renewal_date = DateOnlyField(required=False, allow_null=True)

    class Meta:
            model = Subscription
            fields = '__all__'
            read_only_fields = ('is_active',)

    def validate_renewal_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Renewal date cannot be in the past")
        return value
