from django.db import models

# Create your models here.

class user_detail(models.Model):
	uniqueuserid=models.CharField(max_length=30)
	fname=models.CharField(max_length=15)
	mname=models.CharField(max_length=15)
	lname=models.CharField(max_length=15)
	name=models.CharField(max_length=50)
	mobile=models.CharField(max_length=10)
	email=models.CharField(max_length=30)
	gender=models.CharField(max_length=100)
	password=models.CharField(max_length=30)
	salary=models.CharField(max_length=30)
class tempuser(models.Model):
	uniqueuserid=models.CharField(max_length=30)
	fname=models.CharField(max_length=15)
	mname=models.CharField(max_length=15)
	lname=models.CharField(max_length=15)
	name=models.CharField(max_length=50)
	mobile=models.CharField(max_length=10)
	email=models.CharField(max_length=30)
	gender=models.CharField(max_length=100)
	password=models.CharField(max_length=30)