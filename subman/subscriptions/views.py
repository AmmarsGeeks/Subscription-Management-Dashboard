from django.shortcuts import render
from rest_framework import viewsets
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.utils import timezone
from rest_framework.response import Response



def dashboard(request):
    subscriptions = Subscription.objects.filter(is_active=True).annotate(
        monthly_cost=ExpressionWrapper(
            F('price') / (12 if F('billing_cycle') == 'annual' else 1),
            output_field=FloatField()
        ),
        annual_cost=ExpressionWrapper(
            F('price') * (12 if F('billing_cycle') == 'monthly' else 1),
            output_field=FloatField()
        )
    )
    
    upcoming_renewals = subscriptions.filter(
        renewal_date__lte=timezone.now().date() + timezone.timedelta(days=7)
    )
    
    total_monthly = sum(sub.monthly_cost for sub in subscriptions)
    
    context = {
        'subscriptions': subscriptions,
        'analytics': {
            'total_monthly': total_monthly,
            'upcoming_renewals': upcoming_renewals,
            'annual_savings': calculate_annual_savings(subscriptions)
        }
    }
    return render(request, 'subscriptions/dashboard.html', context)

def calculate_annual_savings(queryset):
    monthly_subs = queryset.filter(billing_cycle='monthly')
    potential_annual = sum(sub.annual_cost for sub in monthly_subs)
    current_annual = sum(sub.price * 12 for sub in monthly_subs)
    return current_annual - potential_annual

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(
            monthly_cost=ExpressionWrapper(
                F('price') / (12 if F('billing_cycle') == 'annual' else 1),
                output_field=FloatField()
            ),
            annual_cost=ExpressionWrapper(
                F('price') * (12 if F('billing_cycle') == 'monthly' else 1),
                output_field=FloatField()
            )
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_monthly = sum(sub.monthly_cost for sub in self.get_queryset())
        upcoming_renewals = self.get_queryset().filter(
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
                'annual_savings': self.calculate_annual_savings()
            }
        }
        return response

    def calculate_annual_savings(self):
        monthly_subs = self.get_queryset().filter(billing_cycle='monthly')
        potential_annual = sum(sub.annual_cost for sub in monthly_subs)
        current_annual = sum(sub.price * 12 for sub in monthly_subs)
        return current_annual - potential_annual