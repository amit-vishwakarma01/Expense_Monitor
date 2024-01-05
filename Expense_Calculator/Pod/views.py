from django.shortcuts import render,redirect
from.models import Pod_detail,pod_member,Pod_transaction
from authentication.models import user_detail,tempuser
from Expenses.models import expense_type
from datetime import date
import random
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
def pods(request):
	if(request.session.get('user')):
		error=''
		if(request.session.get('error')):
			error=request.session.get('error')
			del request.session['error']
		pids=set()
		pods=pod_member.objects.filter(useruniqueid=request.session.get('user'))
		for i in pods:
			pids.add(i.podid)
		res=Pod_detail.objects.filter(podid__in=pids,status='Active')
		if(len(res)>0):
			return render(request,'pods.html',{'res':res,'error':error})
		return render(request,'pods.html',{'errors':'No Active Sharing Groups are available.'})
	return redirect('login')
def addpod(request):
	if(request.session.get('user')):
		return render(request,'add_pods.html')
	return redirect('login')

def addingpod(request):
	if(request.session.get('user')):
		userdetail=user_detail.objects.filter(uniqueuserid=request.session.get('user'))
		podname=request.POST['podname']
		status='Active'
		createddate= date.today()
		lastmodifiedddate= date.today()
		podid=random.randint(100000000,999999999)
		while(len(Pod_detail.objects.filter(podid=podid))==1):
			podid=random.randint(100000000,999999999)
		name=userdetail[0].fname
		if(userdetail[0].mname):
			name+=' '+userdetail[0].mname
		if(userdetail[0].lname):
			name+=' '+userdetail[0].lname
		res=Pod_detail(podid=podid,status=status,pod_name=podname,createdby=name,lastmodifiedby=name,createddate=createddate,lastmodifiedddate=lastmodifiedddate)
		res.save()
		podmemberid=random.randint(100000000,999999999)
		while(len(pod_member.objects.filter(podmemberid=podmemberid))==1):
			podmemberid=random.randint(100000000,999999999)
		res1=pod_member(podmemberid=podmemberid, podid=podid,name=name,email=userdetail[0].email,mobile=userdetail[0].mobile,useruniqueid=request.session.get('user'))
		res1.save()
		return redirect('pods')
	return redirect('login')

def poddetail(request):
	if(request.session.get('user')):
		if(request.session.get('podid')):
			podid=request.session.get('podid')
		else:
			podid=request.GET['id']
		username=user_detail.objects.filter(uniqueuserid=request.session.get('user'))
		usernames=username[0].name
		res=Pod_detail.objects.filter(podid=podid)
		podname=''
		podcreateuser=''
		if(len(res)>0):
			podname=res[0].pod_name
			podcreateuser=res[0].createdby

		print(usernames+podcreateuser)
		res2=pod_member.objects.filter(podid=podid)
		res1=Pod_transaction.objects.filter(podid=podid)
		total=0
		for i in res1:
			total+=i.amount
		error=''
		memberamountlist=prepareresponse(res2,res1,total)
		if(request.session.get('error')):
			error=request.session.get('error')
			del request.session['error']
		if(len(res)>0 and len(res2)>0 and error==''):
			return render(request,'poddetail.html',{'res':res,'errors':'No Transaction available','res2':res2,'podid':podid,'podowner':podcreateuser,'currentuser':usernames,'res1':res1,'total':total,'memberamountlist':memberamountlist,'podname':podname})
		elif(len(res)>0 and len(res2)>0 and error!=''):
			return render(request,'poddetail.html',{'res':res,'error':error,'res2':res2,'podid':podid,'podowner':podcreateuser,'currentuser':usernames,'res1':res1,'total':total,'memberamountlist':memberamountlist,'podname':podname})
		return redirect('pods')
	return redirect('login')
def prepareresponse(membername,transactionlist,alltotal):
	memberlist=[]
	
	for i in membername:
		d=dict()
		total=0
		d['name']=i.name
		d['Split']=(alltotal)/len(membername)
		d['totalpaid']=total
		d['pending']=(alltotal)/len(membername)-total
		d['useruniqueid']=i.useruniqueid
		for j in transactionlist:
			if(i.name == j.podmemberName):
				total+=j.amount
			d['totalpaid']=total
			d['pending']=(alltotal)/len(membername)-total
			d['Split']=(alltotal)/len(membername)
		memberlist.append(d)
	if(len(memberlist)==0):
		return None
	return memberlist
def searchmember(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		return render(request,'searchscreen.html',{'podid':podid})
	return redirect('login')
def searchmemberdetail(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		searchname=request.POST['name']
		res=user_detail.objects.filter(name__contains=searchname).values()
		mode=1
		return render(request,'searchscreen.html',{'podid':podid,'res':res,'len':mode})
	return redirect('login')
def adduser(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		userid=request.GET['userid']
		if(len(pod_member.objects.filter(podid=podid,useruniqueid=userid))==0):
			podmemberid=random.randint(100000000,999999999)
			user=user_detail.objects.filter(uniqueuserid=userid)
			while(len(pod_member.objects.filter(podmemberid=podmemberid))==1):
				podmemberid=random.randint(100000000,999999999)
			res1=pod_member(podmemberid=podmemberid, podid=podid,name=user[0].name,email=user[0].email,mobile=user[0].mobile,useruniqueid=userid)
			res1.save()
			return render(request,'searchscreen.html',{'podid':podid,'errors':'User Added Successfully.'})
		elif(len(pod_member.objects.filter(podid=podid,useruniqueid=userid))==1):
			return render(request,'searchscreen.html',{'podid':podid,'errors':'User is already Added to Group'})
		else:
			return render(request,'searchscreen.html',{'podid':podid,'errors':'Some Error occured while adding user to Group. Please contact to admin.'})

	return redirect('login')

def removeuser(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		userid=request.GET['userid']
		request.session['podid']=podid
		if(userid==request.session.get('user')):
			request.session['error']='You can not delete own user from POd as you are the owner of POD.'
			return redirect('pods')
			return render(request,'poddetail.html',{'error':'You can not delete own user from POd as you are the owner of POD.'})
		else:
			pod_member.objects.filter(podid=podid,useruniqueid=userid).delete()
			request.session['error']='POD Member deleted Successfully.'
			return redirect('pods')
			return render(request,'poddetail.html',{'error':'POD Member deleted Successfully.'})

	return redirect('login')

def addtransaction(request):
	if(request.session.get('user')):
		us=user_detail.objects.filter(uniqueuserid=request.session.get('user'))
		podid=request.GET['searchid']
		res1=Pod_detail.objects.filter(podid=podid)
		res2=pod_member.objects.filter(podid=podid)
		podname=res1[0].pod_name
		print(podname)
		exname=expense_type.objects.all()
		return render(request,'showtransactionform.html',{'res1':podid,'res':exname,'podname':podname,'res2':res2,'current':us[0].name})
	return redirect('login')

def addtransactiondata(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		Expensetype=request.POST['Type']
		Expensename=request.POST['Expensename']
		date=request.POST['date']
		amount=request.POST['amount']
		payment_mode=request.POST['payment_mode']
		Payeename=request.POST['Payeename']
		transid=random.randint(100000000,999999999)
		while(len(Pod_transaction.objects.filter(podid=podid,transid=transid))==1):
			transid=random.randint(100000000,999999999)
		podmember=pod_member.objects.filter(useruniqueid=request.session.get('user'))
		res= Pod_transaction(transid=transid,podmemberid=podmember[0].podmemberid,name=Expensename,useruniqueid=request.session.get('user'),podmemberName=Payeename,podid=podid,amount=amount,expensetype=Expensetype,transactionmode=payment_mode,transactiondate=date)
		res.save()
		request.session['podid']=podid
		return redirect('poddetail')
	return redirect('login')

def updategroupdetail(request):
	if(request.session.get('user')):
		searchid=request.GET['searchid']
		podname=request.POST['podname']
		userdetail=user_detail.objects.filter(uniqueuserid=request.session.get('user'))
		name=userdetail[0].fname
		if(userdetail[0].mname):
			name+=' '+userdetail[0].mname
		if(userdetail[0].lname):
			name+=' '+userdetail[0].lname
		lastmodifiedddate= date.today()
		res=Pod_detail.objects.get(podid=searchid)
		res.lastmodifiedby=name
		res.lastmodifiedddate=lastmodifiedddate
		res.pod_name=podname
		res.save()
		return redirect('pods')
	return redirect('login')

def deletegroup(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		res=pod_member.objects.filter(podid=podid)
		for i in res:
			sememberid=(i.useruniqueid)
			tempuser.objects.filter(uniqueuserid__contains=sememberid).delete()
		pod_member.objects.filter(podid=podid).delete()
		Pod_detail.objects.filter(podid=podid).delete()
		Pod_transaction.objects.filter(podid=podid).delete()
		return redirect('pods')
	return redirect('login')

def viewtransaction(request):
	if(request.session.get('user')):
		podid=request.GET['podid']
		podmemberid=request.GET['podmemberid']
		transid=request.GET['transid']
		res=expense_type.objects.all()
		res2=pod_member.objects.filter(podid=podid)
		res1=Pod_transaction.objects.filter(podid=podid,podmemberid=podmemberid,transid=transid)
		us=res1[0].podmemberName
		print(us)
		print(res2[1].name)
		podname=Pod_detail.objects.filter(podid=podid)[0].pod_name
		res.exclude(expense_type=res1[0].expensetype)
		print(res)
		owner=False
		if(res1[0].useruniqueid==request.session.get('user')):
			owner=True
		return render(request,'viewtransaction.html',{'res':res,'res1':res1,'owner':owner,'podname':podname,'res2':res2,'current':us})
	return redirect('login')

def Updatetransaction(request):
	if(request.session.get('user')):
		podid=request.GET['podid']
		transid=request.GET['transid']
		Expensetype=request.POST['Type']
		Expensename=request.POST['Expensename']
		date=request.POST['date']
		amount=request.POST['amount']
		payment_mode=request.POST['payment_mode']
		Payeename=request.POST['Payeename']
		res=Pod_transaction.objects.get(podid=podid,transid=transid)
		res.expensetype=Expensetype
		res.name=Expensename
		res.transactiondate=date
		res.amount=amount
		res.transactionmode=payment_mode
		res.podmemberName=Payeename
		res.save()
		request.session['podid']=podid
		return redirect('poddetail')
	return redirect('login')

def deletepodtransaction(request):
	if(request.session.get('user')):
		podid=request.GET['podid']
		transid=request.GET['transid']
		Pod_transaction.objects.filter(podid=podid,transid=transid).delete()
		request.session['podid']=podid
		return redirect('poddetail')
	return redirect('login')

def sendmail(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		res=Pod_detail.objects.filter(podid=podid)
		res2=pod_member.objects.filter(podid=podid)
		res1=Pod_transaction.objects.filter(podid=podid)
		subject = 'Expense detail for Group Name: '+res[0].pod_name
		for i in res2:
			if(i.useruniqueid!=request.session.get('user')):
				total=0
				for j in res1:
					total+=j.amount
				memberamountlist=prepareresponse(res2,res1,total)
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [i.email]
				html_message = render_to_string('podmail_template.html', {'res1': res1,'res':res,'total':total,'memberamountlist':memberamountlist})
				plain_message = strip_tags(html_message)
				if(not mail.send_mail( subject,plain_message,email_from,recipient_list , html_message=html_message,fail_silently=False)):
					request.session['error']='Some Error Occured while sending mail to '+str(i.email)+' please contact to Admin.'
		request.session['error']='Email send Successfully to all users.'			
		return redirect('pods')
	return redirect('login')

def showtempuserform(request):
	if(request.session.get('user')):
		podid=request.GET['searchid']
		return render(request,'showtempuserform.html',{'podid':podid})

	return redirect('login')