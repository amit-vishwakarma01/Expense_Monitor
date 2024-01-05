from django.shortcuts import render,redirect
import random
from Expenses.models import query
def index(request):
	if request.session.get('user'):
		return redirect('dashboard')
	error=""
	if request.session.get('error'):
		error=request.session.get('error')
		del request.session['error']
	return render(request,'index.html',{'error':error})

def home(request):
	if request.session.get('user'):
		return redirect('dashboard')
	return redirect('index')	

def submitquery1(request):
	email=request.POST['email']
	subject=request.POST['query_type']
	description=request.POST['description']
	queryid=random.randint(100000,999999)
	while(len(query.objects.filter(queryid=queryid))==1):
		queryid=random.randint(100000,999999)
	res=query(queryid=queryid,email=email,subject=subject,description=description)
	res.save()
	request.session['error']="Your Query Submitted Successfully.Team member will contact you soon.\nThank you."
	return redirect('index')