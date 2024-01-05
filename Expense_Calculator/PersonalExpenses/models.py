from django.db import models
# Create your models here.
class personal_group(models.Model):
    groupid=models.IntegerField()
    groupname=models.CharField(max_length=100)
    personname=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    createdate=models.DateField()
    createdbyid=models.CharField(max_length=50)
class transaction(models.Model):
    transid=models.IntegerField()
    groupid=models.IntegerField()
    name=models.CharField(max_length=30)
    paymentmode=models.CharField(max_length=20)
    reason=models.CharField(max_length=100)
    amount=models.FloatField()
    createdate=models.DateField()
