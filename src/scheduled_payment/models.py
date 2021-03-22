from django.db import models
from account.models import Account
from transfer.models import Transfer
from django.core.validators import MaxValueValidator, MinValueValidator
from _datetime import datetime
import calendar

class ScheduledPayment(models.Model):
    due_at = models.fields.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(31)
    ])
    from_account = models.ForeignKey(Account, models.CASCADE, related_name='spayments_in')
    to_account = models.ForeignKey(Account, models.CASCADE, related_name='spayments_out')
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    @staticmethod
    def check_due():
        today_date = datetime.today().day
        _, last_month_day = calendar.monthrange(datetime.today().year, datetime.today().month)
        if today_date == last_month_day:
            return ScheduledPayment.objects.filter(due_at__gte=today_date)
        else:
            return ScheduledPayment.objects.filter(due_at=today_date)

    def create_transfer(self):
        return Transfer.do_transfer(self.from_account, self.to_account, self.amount)