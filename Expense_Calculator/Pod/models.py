from django.db import models
import  datetime
# Create your models here.
class Pod_detail(models.Model):
    podid=models.IntegerField()
    pod_name=models.CharField(max_length=50)
    createdby=models.CharField(max_length=50)
    lastmodifiedby=models.CharField(max_length=50)
    lastmodifiedddate=models.DateField(default=datetime.date.today)
    createddate=models.DateField()
    status=models.CharField(max_length=30)

class pod_member(models.Model):
    podmemberid=models.IntegerField()
    podid=models.IntegerField()
    useruniqueid=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)

class Pod_transaction(models.Model):
    podmemberid=models.IntegerField()
    transid=models.CharField(max_length=30)
    name=models.CharField(max_length=50)
    useruniqueid=models.CharField(max_length=30)
    podmemberName=models.CharField(max_length=50)
    podid=models.IntegerField()
    amount=models.FloatField()
    expensetype=models.CharField(max_length=50)
    transactionmode=models.CharField(max_length=30)
    transactiondate=models.DateField()