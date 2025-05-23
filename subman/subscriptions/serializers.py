from rest_framework import serializers
from .models import Subscription
from django.utils import timezone

class SubscriptionSerializer(serializers.ModelSerializer):
    monthly_cost = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    annual_cost = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('renewal_date', 'is_active')

    def validate_renewal_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Renewal date cannot be in the past")
        return value