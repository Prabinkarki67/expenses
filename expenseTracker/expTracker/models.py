from django.db import models
from datetime import datetime
# Create your models here.


class Accounts(models.Model):
    name = models.CharField(max_length = 100)
    expense = models.FLoatField(default = 0)
    user = models.ForeignKey('auth.User', on_delete= models.CASCADE)
    expense_list = models.ManyToManyField('Expense' )