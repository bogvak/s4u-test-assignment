from decimal import Decimal
from django.db import models
from account.models import Account
from django.db import transaction

class InsufficientBalance(Exception):
    pass

class ImproperTransferAmount(Exception):
    pass

class Transfer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_account = models.ForeignKey(Account, models.CASCADE, related_name='transfers_in')
    to_account = models.ForeignKey(Account, models.CASCADE, related_name='transfers_out')
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    @staticmethod
    def do_transfer(from_account: Account, to_account: Account, amount: Decimal):
        if amount <= 0:
            raise ImproperTransferAmount()

        if from_account.balance < amount:
            raise InsufficientBalance()

        with transaction.atomic():
            locked_from_account = Account.objects.select_for_update().get(number=from_account.number)
            locked_to_account = Account.objects.select_for_update().get(number=to_account.number)
            locked_from_account.balance -= amount
            locked_to_account.balance += amount
            locked_from_account.save()
            locked_to_account.save()

        # from_account.balance -= amount
        # to_account.balance += amount
        # from_account.save()
        # to_account.save()

        return Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

# Account / transfer schema evolution comments
# External accounts
# 1. Modify Account scheme with additional fields type - it will describe if account is external or internal
#    Depending on if all external accounts have universal transfer API 0 it could simple attribute like 'external' or different types - definied what transfer procedure should be used
# 2. Introduce another sheme for external accounts those will have universal attributes of external accounts - Bank ID, IBAN etc - if it's appropriate
# 3. Introduce methods to transfer for conducting external transfer - universal if it's possible or multiple methods ot multiple - if transfer procedures are vary
#
# Cash operation
# 1. Creating another field defiining type of operation - account-to-account or cash <-> account or etc
# 2. Introducing methods those are implementing cash operations - execute appropriate procedure based on operation_type field value