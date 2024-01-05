from django.shortcuts import render,redirect
from authentication.models import user_detail
from django.http import HttpResponseRedirect
from .models import expense_type,expense_detail,query,replies
from authentication.models import tempuser
import datetime,random
from datetime import date
# Create your views here.

def delete(request):
	if request.session.get('user'):
		expenseid=request.GET['ex']
		expense_detail.objects.filter(email=request.session.get('user'),expenseid=expenseid).delete()
		request.session['error']="Expense Deleted Succssfully."
		return redirect('dashboard')
def submitquery(request):
	if request.session.get('user'):
		email=user_detail.objects.filter(uniqueuserid=request.session.get('user'))[0].email
		subject=request.POST['query_type']
		description=request.POST['description']
		queryid=random.randint(100000,999999)
		while(len(query.objects.filter(queryid=queryid))==1):
			queryid=random.randint(100000,999999)
		res=query(queryid=queryid,email=email,subject=subject,description=description)
		res.save()
		request.session['error']="Your Query Submitted Successfully.Team member will contact you soon.\nThank you."
		return redirect('contact')
	return redirect('login')
def contact(request):
	if request.session.get('user'):
		error=""
		if request.session.get('error'):
			error=request.session.get('error')
			del request.session['error']
		res=user_detail.objects.filter(uniqueuserid=request.session.get('user'))
		return render(request,'contact.html',{'email':res[0].email,'error':error})
def expense(request):
	if request.session.get('user'):
		email=request.session.get('user')
		res1=expense_type.objects.all()
		detail=user_detail.objects.filter(uniqueuserid=email)
		res=expense_detail.objects.filter(email=detail[0].email)
		total=0
		todays_date = date.today()
		content=[]
		for i in res1:
			total=0
			for j in res:
				if j.expensename==i.expense_type:
					total+=int(j.amount)
			content.append(total)
		for i in res:
			total+=int(i.amount)
		remain=int(detail[0].salary)-total
		if(remain<0):
			remain="Budget Exceeds "+"("+str(remain)+")"
		return render(request,"showexpense.html",{'todays_date':todays_date,'content':content,'remain':remain,'res':res,'detail':detail,'res1':res1,'total':total,'range':range(2000,2051)})

	return redirect('login')
def dashboard(request):
	if request.session.get('user'):
		res=expense_type.objects.all()
		error=""
		if request.session.get('error'):
			error=request.session.get('error')
			del request.session['error']
		res1=expense_detail.objects.filter(email=user_detail.objects.filter(uniqueuserid=request.session.get('user'))[0].email)
		todays_date = date.today()
		year=todays_date.year
		month=todays_date.month
		months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
		m={"1":"Jan","2":"Feb","3":"Mar","4":"Apr","5":"May","6":"Jun","7":"Jul","8":"Aug","9":"Sep","10":"Oct","11":"Nov","12":"Dec"}
		
		months1=[]
		res2=res1.filter(year=year)
		res3=res1.filter(year=year,month=month)
		month=m[str(month)]
		for j in range(1,13):
			total=0
			for i in res2:
				
				if int(i.month)==j:
					total+=int(i.amount)
			months1.append(total)
		content=[]
		for i in res:
			total=0
			for j in res3:
				if j.expensename==i.expense_type:
					total+=int(j.amount)
					
			content.append(total)
		
		#
		dummy=[]
		for i in res1:
			if i.year not in dummy:
				dummy.append(i.year)
		value=[]
		for i in dummy:
			total=0
			for j in res1:
				if j.year==i:
					total+=int(j.amount)
			value.append(total)

		return render(request,'dashboard.html',{'month':month,'year':year,'years':dummy,'value':value,'months1':months1,'months':months,'res':res,'range':range(2000,2051),'error':error,'content':content})
	else:
		return redirect('login')
def profile(request):
	if request.session.get('user'):
		email=request.session.get('user')
		if(request.GET['userid']==email):
			return redirect('myprofile')
		email=request.GET['userid']
		res=user_detail.objects.filter(uniqueuserid=email)
		if(len(res)==0):
			res=tempuser.objects.filter(uniqueuserid=email)
		errors=""
		if request.session.get('error'):
			errors=request.session.get('error')
			del request.session['error']
		return render(request,'myprofile.html',{'res':res,'error':errors,'check':True})
	return redirect('login')
def myprofile(request):
	if request.session.get('user'):
		email=request.session.get('user')
		res=user_detail.objects.filter(uniqueuserid=email)
		errors=""
		if request.session.get('error'):
			errors=request.session.get('error')
			del request.session['error']
		return render(request,'myprofile.html',{'res':res,'error':errors})
	return redirect('login')
def addexpense(request):
	if request.session.get('user'):
		error=""
		if request.session.get('error'):
			error=request.session.get('error')
			del request.session['error']
		res=expense_type.objects.all()
		return render(request,'additem.html',{'res':res,'error':error})
	return redirect('login')
def addingitem(request):
	if request.session.get('user'):
		expenseid=random.randint(100000000,999999999)
		while(len(expense_detail.objects.filter(expenseid=expenseid))==1):
			expenseid=random.randint(100000000,999999999)
		email=user_detail.objects.filter(uniqueuserid=request.session.get('user'))[0].email
		Type=request.POST['Type']
		date=request.POST['date']
		amount=request.POST['amount']
		mode=request.POST['payment_mode']
		datem = datetime.datetime.strptime(date, "%Y-%m-%d")
		days=datem.day       # 25
		months=datem.month      # 5
		years=datem.year       # 2021
		res=expense_detail(expenseid=expenseid,email=email,expensename=Type,amount=amount,day=days,month=months,year=years,typeofpayment=mode)
		res.save()
		request.session['error']="Expense Added Successfully"
		return redirect('addexpense')
	return redirect('login')

def showexpense(request):
	if request.session.get('user'):
		lst={}
		email=request.session.get('user')
		res1=expense_type.objects.all()
		detail=user_detail.objects.filter(uniqueuserid=email)
		res=expense_detail.objects.filter(email=detail[0].email)
		print(len(res))
		todays_date = date.today()
		day=0
		month=0
		year=0
		if(request.GET['Type'] or request.GET['day'] or request.GET['month'] or request.GET['year'] or request.GET['payment_mode']):
			if request.GET['Type'] !="0":
				res=res.filter(expensename=request.GET['Type'])
				#lst[expensename]=request.GET['Type']
				
			if request.GET['day'] !="0":
				res=res.filter(day=request.GET['day'])
				day=request.GET['day']
				lst[day]=request.GET['day']
				
			if request.GET['month'] !="0":
				res=res.filter(month=request.GET['month'])
				month=request.GET['month']
				
			if request.GET['year'] !="0":
				res=res.filter(year=request.GET['year'])
				year=request.GET['year']
				
			if request.GET['amount'] !="":
				res=res.filter(amount=request.GET['amount'])
				
			if request.GET['payment_mode'] !="0":
				res=res.filter(typeofpayment=request.GET['payment_mode'])
			
		
		content=[]
		for i in res1:
			total=0
			for j in res:
				if j.expensename==i.expense_type:
					total+=int(j.amount)
			content.append(total)
		'''res=expense_detail.objects.filter(email=email)'''
		total=0
		for i in res:
			total+=int(i.amount)
		remain=int(detail[0].salary)-total
		if(remain<0):
			remain="Budget Exceeds "+"("+str(remain)+")"
		return render(request,"showexpense.html",{'todays_date':todays_date,'content':content,'day':day,'month':month,'year':year,'remain':remain,'res':res,'detail':detail,'res1':res1,'total':total,'range':range(2000,2051)})
	return redirect('login')

def showexpensebydate(request):
	if request.session.get('user'):
		res1=expense_type.objects.all()
		email=request.session.get('user')
		detail=user_detail.objects.filter(email=email)
		date1=request.GET['date1']
		date2=request.GET['date2']
		datem1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
		day1=datem1.day       # 25
		month1=datem1.month      # 5
		year1=datem1.year
		datem2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
		day2=datem2.day       # 25
		month2=datem2.month      # 5
		year2=datem2.year
		res=expense_detail.objects.filter(email=email,day__gte=day1 , day__lte=day2,month__gte=month1 , month__lte=month2,year__gte=year1 ,year__lte=year2)
		
		total=0
		check=1
		import re
		date1=re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', date1)
		date2=re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', date2)
		content=[]
		for i in res1:
			total=0
			for j in res:
				if j.expensename==i.expense_type:
					total+=int(j.amount)
			content.append(total)
		total=0
		for i in res:
			total+=int(i.amount)
		remain=int(detail[0].salary)-total
		if(remain<0):
			remain="Budget Exceeds "+"("+str(remain)+")"

		return render(request,"showexpense.html",{'content':content,'remain':remain,'check':check,'date1':date1,'date2':date2,'res':res,'detail':detail,'res1':res1,'total':total,range:range(2000,2051)})
	return redirect('login')







def edit(request):
	if request.session.get('user'):
		expenseid=request.GET['ex']
		res=expense_type.objects.all()
		res1=expense_detail.objects.filter(expenseid=expenseid)
		d = datetime.datetime(int(res1[0].year), int(res1[0].month), int(res1[0].day))
		date = str(d.date())
		print(date)
		return render(request,'edit.html',{'res':res,'res1':res1,'date':date})
	return redirect('login')

def update_item(request):
	if request.session.get('user'):
		expenseid=request.POST['expenseid']
		email=user_detail.objects.filter(uniqueuserid=request.session.get('user'))[0].email
		Type=request.POST['Type']
		date=request.POST['date']
		amount=request.POST['amount']
		mode=request.POST['payment_mode']
		datem = datetime.datetime.strptime(date, "%Y-%m-%d")
		days=datem.day       # 25
		months=datem.month      # 5
		years=datem.year
		#expenseid=expenseid,email=email,expensename=Type,amount=amount,day=days,month=months,
		#year=years,typeofpayment=mode
		data=expense_detail.objects.get(email=email,expenseid=expenseid)
		data.expensename=Type
		data.amount=amount
		data.day=days
		data.month=months
		data.year=years
		data.typeofpayment=mode
		data.save()
		request.session['error']="Expense Detail Updated Succssfully."
		return redirect('dashboard')
	return redirect('login')


def deleteaccount(request):
	if request.session.get('user'):
		email=request.session.get('user')
		expense_detail.objects.filter(email=user_detail.objects.filter(uniqueuserid=email)[0].email).delete()
		query.objects.filter(email=user_detail.objects.filter(uniqueuserid=email)[0].email).delete()
		replies.objects.filter(email=user_detail.objects.filter(uniqueuserid=email)[0].email).delete()
		user_detail.objects.filter(uniqueuserid=email).delete()
		del request.session['user']
		return render(request,"deleting_account.html")

	return redirect('dashboard')












def userquery(request):
	if request.session.get('user'):
		res=query.objects.filter(email=user_detail.objects.filter(uniqueuserid=request.session.get('user'))[0].email)
		return render(request,"userquery.html",{'res':res})
	return redirect('dashboard')

def userreply(request):
	if request.session.get('user'):
		qid=request.GET['qid']
		res=query.objects.filter(queryid=qid)
		res1=replies.objects.filter(queryid=qid)
		return render(request,"userreply.html",{'res':res,'res1':res1})
	return redirect('dashboard')
def senduserreply(request):
	if request.session.get('user'):
		queryid=request.POST['queryid']
		subject=request.POST['subject']
		email=request.POST['email']
		rdescription=request.POST['rdescription']
		#description=request.POST['description']
		replyid=random.randint(100000,999999)
		while(len(replies.objects.filter(replyid=replyid))==1):
			replyid=random.randint(100000,999999)
		res=replies(queryid=queryid,email=email,replymode="User",replyid=replyid,subject=subject,description=rdescription)
		res.save()
		return HttpResponseRedirect("userreply?qid="+queryid)
	return redirect('dashboard')


def userclose(request):
	if request.session.get('user'):
		qid=request.GET['qid']
		query.objects.filter(queryid=qid).delete()
		replies.objects.filter(queryid=qid).delete()
		return redirect('userquery')
	return redirect('dashboard')

