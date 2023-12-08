from decimal import Decimal
from django.db import models


# Here are my models.

# ----CUSTOMER_ACCOUNT------#
class CompteMobileClient(models.Model):
    id_cl = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=30)
    SoldeMobile = models.DecimalField(max_digits=5,decimal_places=3,default=Decimal('0.000'))
    password = models.CharField(max_length=5)


# ----Operation------#
class Operation(models.Model):
    id_op = models.AutoField(primary_key=True)
    montant = models.DecimalField(max_digits=4,decimal_places=2,default=Decimal('0.00'))
    date_operation = models.DateField(auto_now=True)
    client = models.ForeignKey(CompteMobileClient, on_delete=models.CASCADE)