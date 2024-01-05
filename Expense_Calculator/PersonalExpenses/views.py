from django.shortcuts import render,redirect
from .models import personal_group,transaction
from datetime import datetime
import random
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def personaldashboard(request):
    if(request.session.get('user')):
        error=''
        if(request.session.get('error')):
            error=request.session.get('error')
            del request.session['error']
        res=personal_group.objects.filter(createdbyid=request.session.get('user'))
        return render(request,'PersonalExpensepages/dashboard.html',{'res':res,'error':error})
    return redirect('login')
def viewgroup(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        res=personal_group.objects.filter(groupid=groupid)
        res1=transaction.objects.filter(groupid=groupid)
        total=0
        length=False
        for i in res1:
            total+=i.amount
        if(len(res1)>0):
            length=True
        if(res[0].createdbyid==request.session.get('user')):
            return render(request,'PersonalExpensepages/groupdetail.html',{'res':res,'groupid':groupid,'res1':res1,'total':total,'len':length})
        return redirect('personaldashboard')
    return redirect('login')
def showaddpersonform(request):
    if(request.session.get('user')):
        return render(request,'PersonalExpensepages/showaddpersonform.html')
    return redirect('login')

def addgroup(request):
    if(request.session.get('user')):
        groupname=request.POST['groupname']
        personname=request.POST['personname']
        mobile=request.POST['mobile']
        email=request.POST['email']
        createddate= date.today()
        groupid=random.randint(100000000,999999999)
        while(len(personal_group.objects.filter(groupid=groupid))==1):
            groupid=random.randint(100000000,999999999)
        res=personal_group(groupid=groupid,groupname=groupname,personname=personname,email=email,phone=mobile,createdate=createddate,createdbyid=request.session.get('user'))
        res.save()
        request.session['error']="Group has been created with Groupname: "+groupname
        return redirect('personaldashboard')
    return redirect('login')

def addtransaction(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        return render(request,'PersonalExpensepages/showaddtransaction.html',{'groupid':groupid})
    return redirect('login')

def addtrans(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        transname=request.POST['name']
        reason=request.POST['reason']
        payment_mode=request.POST['payment_mode']
        amount=request.POST['amount']
        date=request.POST['date']
        transid=random.randint(100000000,999999999)
        while(len(transaction.objects.filter(groupid=groupid,transid=transid))==1):
            transid=random.randint(100000000,999999999)
        res=transaction(groupid=groupid,transid=transid,name=transname,paymentmode=payment_mode,amount=amount,createdate=date,reason=reason)
        res.save()
        request.session['error']="Transaction on Group(id="+str(groupid)+") with transactionid "+str(transid)+" has been created successfully."
        return redirect('personaldashboard')

    return redirect('login')

def viewtrans(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        transid=request.GET['transid']
        res=transaction.objects.filter(groupid=groupid,transid=transid)
        date=str(res[0].createdate)
        return render(request,'PersonalExpensepages/showtransaction.html',{'res':res,'transid':transid,'date':date})
    return redirect('login')

def deletetrans(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        transid=request.GET['transid']
        transaction.objects.filter(groupid=groupid,transid=transid).delete()
        request.session['error']="Transaction with Transaction id "+str(transid)+" has been deleted successfully."
        return redirect('personaldashboard')
    return redirect('login')
def updatetrans(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        transid=request.GET['transid']
        transname=request.POST['name']
        reason=request.POST['reason']
        payment_mode=request.POST['payment_mode']
        amount=request.POST['amount']
        date=request.POST['date']
        res=transaction.objects.get(groupid=groupid,transid=transid)
        res.name=transname
        res.reason=reason
        res.paymentmode=payment_mode
        res.amount=amount
        res.createdate=date
        res.save()
        request.session['error']="Transaction with Transaction id "+str(transid)+" has been Updated successfully."
        return redirect('personaldashboard')
    return redirect('login')

def editgroup(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        res=personal_group.objects.filter(groupid=groupid)
        return render(request,'PersonalExpensepages/editgroup.html',{'res':res})
    return redirect('login')

def updategroupdetail(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        groupname=request.POST['groupname']
        personname=request.POST['personname']
        mobile=request.POST['mobile']
        email=request.POST['email']
        res=personal_group.objects.get(groupid=groupid)
        res.groupname=groupname
        res.personname=personname
        res.phone=mobile
        res.email=email
        res.save()
        request.session['error']="Group with Group Name: "+groupname+" has been Updated successfully."
        return redirect('personaldashboard')
    return redirect('login')
def deletegroup(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        transaction.objects.filter(groupid=groupid).delete()
        personal_group.objects.filter(groupid=groupid).delete()
        request.session['error']="Group and All transaction has been deleted successfully."
        return redirect('personaldashboard')
    return redirect('login')

def sendemail(request):
    if(request.session.get('user')):
        groupid=request.GET['groupid']
        res=personal_group.objects.filter(groupid=groupid)
        subject = 'Expense detail for Group Name: '+res[0].groupname
        res1=transaction.objects.filter(groupid=groupid)
        amount=0
        for i in res1:
            amount+=i.amount
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [res[0].email]
        html_message = render_to_string('mail_template.html', {'res1': res1,'res':res,'total':amount})
        plain_message = strip_tags(html_message)
        if(mail.send_mail( subject,plain_message,email_from,recipient_list , html_message=html_message,fail_silently=False)):
            print('Mail sent successfully')
            request.session['error']='Email send Successfully to Email address: '+res[0].email
        else:
            request.session['error']='Some Error Occured while sending mail please contact to Admin.'
        return redirect('personaldashboard')
    return redirect('login')