from django.shortcuts import render,redirect
from .models import user_detail,tempuser
from Pod.models import pod_member
import string,random
# Create your views here.

def signup(request):
	return render(request,'signup.html')
def login(request):
	if request.session.get('user'):
		return redirect('dashboard')
	else:
		return render(request,'login.html')
def logout(request):
	del request.session['user']
	return redirect('login')

def register(request):
	fname=request.POST['fname']
	mname=request.POST['mname']
	lname=request.POST['lname']
	gender=request.POST['gender']
	email=request.POST['email']
	mobile=request.POST['mobile']
	password=request.POST['password']
	rpassword=request.POST['rpassword']
	name=fname
	if(request.POST['mname']):
		name+=' '+mname
	if(request.POST['lname']):
		name+=' '+lname
	username=''.join(random.choice(string.ascii_letters) for i in range(20))
	while(len(user_detail.objects.filter(uniqueuserid=username))==1):
		username=''.join(random.choice(string.ascii_letters) for i in range(20))
	if password!=rpassword:
		return render(request,'signup.html',{'error':'Password Does Not matched'})
	else:
		if len(user_detail.objects.filter(email=email))==1:
			return render(request,'signup.html',{'error':'Email is already exist'})
		else:
			res=user_detail(fname=fname,mname=mname,lname=lname,name=name,email=email,mobile=mobile,password=password,gender=gender,salary="0",uniqueuserid=username)
			res.save()
			request.session['user']=username
			return redirect('dashboard')


def authenticate_user(request):
	email=request.POST['email']
	password=request.POST['password']
	if len(user_detail.objects.filter(email=email,password=password))==1:
		user=user_detail.objects.filter(email=email,password=password)
		request.session['user']=user[0].uniqueuserid
		return redirect('dashboard')
	else:
		return render(request,"login.html",{'error':'Email or Password is Incorrect'})
def update_profile(request):
	if request.session.get('user'):
		fname=request.POST['fname']
		mname=request.POST['mname']
		lname=request.POST['lname']
		gender=request.POST['gender']
		email=request.POST['email']
		mobile=request.POST['mobile']
		salary=request.POST['salary']
		name=fname
		if(request.POST['mname']):
			name+=' '+mname
		if(request.POST['lname']):
			name+=' '+lname
		data=user_detail.objects.get(uniqueuserid=request.session.get('user'))
		data.fname=fname
		data.lname=lname
		data.mname=mname
		data.gender=gender
		data.mobile=mobile
		data.salary=salary
		data.name=name
		data.email=email
		data.save()
		request.session['error']="Profile Upadted Successfully."
		return redirect('myprofile')
	else:
		return redirect('login')

def change_password(request):
	if request.session.get('user'):
		return render(request,"change_password.html")
	else:
		return redirect('login')
def updating_password(request):
	if request.session.get('user'):
		password=request.POST['password']
		rpassword=request.POST['rpassword']
		if password==rpassword:
			email=request.session.get('user')
			data=user_detail.objects.get(uniqueuserid=email)
			data.password=password
			data.save()
			del request.session['user']
			return render(request,"processing.html")
		else:
			return render(request,"change_password.html",{'error':'Oops! Both password does not matched.'})
	else:
		return redirect('login')

def tempuserregister(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		fname=request.POST['fname']
		mname=request.POST['mname']
		lname=request.POST['lname']
		gender=request.POST['gender']
		email=request.POST['email']
		mobile=request.POST['mobile']
		name=fname
		if(request.POST['mname']):
			name+=' '+mname
		if(request.POST['lname']):
			name+=' '+lname
		username=''.join(random.choice(string.ascii_letters) for i in range(20))
		password=''.join(random.choice(string.ascii_letters) for i in range(15))
		while(len(tempuser.objects.filter(uniqueuserid=username))==1):
			username=''.join(random.choice(string.ascii_letters) for i in range(20))
		res=tempuser(fname=fname,mname=mname,lname=lname,name=name,email=email,mobile=mobile,password=password,gender=gender,uniqueuserid=username)
		res.save()
		podid=request.GET['searchid']
		userid=username
		if(len(pod_member.objects.filter(podid=podid,useruniqueid=userid))==0):
			podmemberid=random.randint(100000000,999999999)
			user=tempuser.objects.filter(uniqueuserid=userid)
			while(len(pod_member.objects.filter(podmemberid=podmemberid))==1):
				podmemberid=random.randint(100000000,999999999)
		res1=pod_member(podmemberid=podmemberid, podid=podid,name=user[0].name,email=user[0].email,mobile=user[0].mobile,useruniqueid=userid)
		res1.save()
		request.session['error']='Member Added successfully.'
		return redirect('pods')
	return redirect('login')