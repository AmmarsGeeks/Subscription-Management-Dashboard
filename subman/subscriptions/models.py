from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Case, When, Value, FloatField

class Subscription(models.Model):
    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=7, choices=BILLING_CYCLES)
    start_date = models.DateField(default=timezone.now)
    renewal_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.renewal_date < timezone.now().date():
            raise ValidationError("Renewal date cannot be in the past")

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            delta = relativedelta(months=1) if self.billing_cycle == 'monthly' else relativedelta(years=1)
            self.renewal_date = self.start_date + delta
        super().save(*args, **kwargs)

    # These are now methods instead of properties for queryset use
    def get_monthly_cost(self):
        return float(self.price) if self.billing_cycle == 'monthly' else float(self.price) / 12

    def get_annual_cost(self):
        return float(self.price) * 12 if self.billing_cycle == 'monthly' else float(self.price)