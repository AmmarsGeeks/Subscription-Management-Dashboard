from django.shortcuts import render
from rest_framework import viewsets
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.utils import timezone
from decimal import Decimal
from django.db.models import Case, When, Value, DecimalField, ExpressionWrapper, F , Sum
import datetime



#Dashboard

def dashboard(request):
    subscriptions = Subscription.objects.filter(is_active=True).annotate(
        monthly_cost=Case(
            When(billing_cycle='monthly', then=F('price')),
            default=ExpressionWrapper(F('price') / Value(12), output_field=DecimalField(max_digits=10, decimal_places=2)),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        annual_cost=Case(
            When(billing_cycle='monthly', then=ExpressionWrapper(F('price') * Value(12), output_field=DecimalField(max_digits=10, decimal_places=2))),
            default=F('price'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    
    # renwwal within 7 days only
    upcoming_renewals = subscriptions.filter(
        renewal_date__lte=timezone.now().date() + timezone.timedelta(days=7),
        renewal_date__gte=timezone.now().date()  # from today
    ).values('name', 'renewal_date', 'price')

    total_monthly = subscriptions.aggregate(
        total=Sum('monthly_cost')
    )['total'] or 0
    
    context = {
        'subscriptions': subscriptions,       
        'analytics': {
            'total_monthly': total_monthly,
            'upcoming_renewals': upcoming_renewals,   
            'annual_savings': calculate_annual_savings(subscriptions)
        }
    }
    return render(request, 'subscriptions/dashboard.html', context)

#Calcualte Annual Saving

def calculate_annual_savings(queryset):
    #Discount 10% for annual year
    discount_rate = Decimal('0.10')
    savings = Decimal('0.0')

    monthly_subs = queryset.filter(billing_cycle='monthly')
    for sub in monthly_subs:
        monthly_annual_cost = sub.price * 12  
        discounted_annual_cost = monthly_annual_cost * (1 - discount_rate) 
        savings += monthly_annual_cost - discounted_annual_cost  

    return savings



class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            monthly_cost=Case(
                When(billing_cycle='monthly', then=F('price')),
                When(billing_cycle='annual', then=ExpressionWrapper(F('price') / Value(12), output_field=DecimalField(max_digits=10, decimal_places=2))),
                default=Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            annual_cost=Case(
                When(billing_cycle='monthly', then=ExpressionWrapper(F('price') * Value(12), output_field=DecimalField(max_digits=10, decimal_places=2))),
                When(billing_cycle='annual', then=F('price')),
                default=Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for obj in queryset:
            if hasattr(obj, 'renewal_date') and isinstance(obj.renewal_date, datetime.datetime):
                obj.renewal_date = obj.renewal_date.date()
        response = super().list(request, *args, **kwargs)
        total_monthly = sum(sub.monthly_cost for sub in queryset)
        upcoming_renewals = queryset.filter(
            renewal_date__lte=timezone.now().date() + timezone.timedelta(days=7)
        )

        response.data = {
            'subscriptions': response.data,
            'analytics': {
                'total_monthly': total_monthly,
                'upcoming_renewals': [
                    {'name': sub.name, 'date': sub.renewal_date, 'amount': sub.price}
                    for sub in upcoming_renewals
                ],
                'annual_savings': self.calculate_annual_savings(queryset)
            }
        }
        return response

    def perform_create(self, serializer):
        instance = serializer.save()
        if isinstance(instance.renewal_date, datetime.datetime):
            instance.renewal_date = instance.renewal_date.date()
        instance.save()

    def calculate_annual_savings(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        monthly_subs = queryset.filter(billing_cycle='monthly')
        potential_annual = sum(sub.annual_cost for sub in monthly_subs)  # decimal
        current_annual = sum(sub.price * Decimal(12) for sub in monthly_subs)  # force Decimal 12
        return current_annual - potential_annual