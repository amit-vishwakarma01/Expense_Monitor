from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from Expenses.models import expense_type,query,replies
# Create your views here.
from .models import admin_login
from authentication.models import user_detail
import random
def adminlogin(request):
	error=""
	if request.session.get('error'):
		error=request.session.get('error')
		del request.session['error']
	return render(request,"admin_login.html",{'error':error})

def validator(request):
	email=request.POST['email']
	password=request.POST['password']
	if len(admin_login.objects.filter(email=email,password=password))==1:
		request.session['admin']=email
		return redirect('admin_panel')
	request.session['error']="Email or Password is incorrect!!!!"
	return redirect('adminlogin')
def admin_panel(request):
	if request.session.get('admin'):
		return render(request,"admindashboard.html")
	return redirect('adminlogin')
def adminlogout(request):
	if request.session.get('admin'):
		del request.session['admin']
	return redirect('adminlogin')
def category(request):
	if request.session.get('admin'):
		cat=expense_type.objects.all()
		return render(request,"addcategory.html",{"cat":cat})
	return redirect('admin_panel')
def addcategory(request):
	if request.session.get('admin'):
		ex=request.POST['category']
		res=expense_type(expense_type=ex)
		res.save()
		return redirect('category')
	return redirect("admin_panel")
def deletetype(request):
	if request.session.get('admin'):
		ex=request.GET['ex']
		expense_type.objects.filter(id=ex).delete()
		return redirect('category')
	return redirect('admin_panel')
def queries(request):
	if request.session.get('admin'):
		res=query.objects.all()
		return render(request,"query.html",{'res':res})
	return redirect('admin_panel')
def reply(request):
	if request.session.get('admin'):
		
		qid=request.GET['qid']
		res=query.objects.filter(queryid=qid)
		email=""
		for i in res:
			email=i.email
		res2=user_detail.objects.filter(email=email)
		res1=replies.objects.filter(queryid=qid)
		return render(request,"reply.html",{'res':res,'res1':res1,'res2':res2})
	return redirect('admin_panel')
def sendreply(request):
	if request.session.get('admin'):
		queryid=request.POST['queryid']
		subject=request.POST['subject']
		email=request.POST['email']
		rdescription=request.POST['rdescription']
		description=request.POST['description']
		replyid=random.randint(100000,999999)
		while(len(replies.objects.filter(replyid=replyid))==1):
			replyid=random.randint(100000,999999)
		res=replies(queryid=queryid,email=email,replymode="Admin",replyid=replyid,subject=subject,description=rdescription)
		res.save()

		return HttpResponseRedirect("reply?qid="+queryid)
	return redirect('admin_panel')
def close(request):
	if request.session.get('admin'):
		qid=request.GET['qid']
		query.objects.filter(queryid=qid).delete()
		replies.objects.filter(queryid=qid).delete()
		return redirect('queries')
	return redirect('admin_panel')