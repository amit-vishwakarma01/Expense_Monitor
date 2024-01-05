from django.db import models

# Create your models here.
class expense_detail(models.Model):
	expenseid=models.CharField(max_length=30)
	email=models.CharField(max_length=30)
	expensename=models.CharField(max_length=100)
	amount=models.CharField(max_length=30)
	day=models.CharField(max_length=30)
	month=models.CharField(max_length=30)
	year=models.CharField(max_length=30)
	typeofpayment=models.CharField(max_length=30)


class expense_type(models.Model):
	expense_type=models.CharField(max_length=30)

class query(models.Model):
	queryid=models.IntegerField()
	email=models.CharField(max_length=30)
	subject=models.CharField(max_length=30)
	description=models.CharField(max_length=1000)
class replies(models.Model):
	queryid=models.IntegerField()
	replyid=models.IntegerField()
	email=models.CharField(max_length=30)
	subject=models.CharField(max_length=30)
	description=models.CharField(max_length=1000)
	replymode=models.CharField(max_length=100,default="")
