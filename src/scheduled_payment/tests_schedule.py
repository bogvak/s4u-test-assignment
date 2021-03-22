from django.test import TestCase

from account.models import Account
from customer.models import Customer
import scheduled_payment.models
from scheduled_payment.models import ScheduledPayment
import unittest.mock
import datetime

class ScheduledPaymentTest(TestCase):
    def setUp(self):
        super(ScheduledPaymentTest, self).setUp()

        customer = Customer.objects.create(
            email='test@test.invalid',
            full_name='Test Customer',
        )

        self.account1 = Account.objects.create(number=123, owner=customer, balance=1000)
        self.account2 = Account.objects.create(number=456, owner=customer, balance=1000)

    def test_basic_schedule_payment(self):
        self.sc = ScheduledPayment.objects.create(due_at=22, from_account=self.account1, to_account=self.account2,
                                                  amount=100)
        self.sc = ScheduledPayment.objects.create(due_at=22, from_account=self.account1, to_account=self.account2,
                                                  amount=50)
        objects = ScheduledPayment.check_due()
        self.assertEqual(len(objects), 2)