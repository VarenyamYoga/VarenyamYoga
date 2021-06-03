import Corporate
from django.shortcuts import render,redirect
from django.views import View
from Corporate.forms import CorporateForm,CorporateInfoForm
from .models import CorporateInfo
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import threading
from django.contrib.sites.shortcuts import get_current_site
from Client.views import EmailThread
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from questions.views import has_group

@login_required(login_url='Corporate-login')
def index(request):
    return render(request,'Corporate/index.html')

class Register(View):
    def get(self,request):
        Corporate_form = CorporateForm()
        Corporate_info_form = CorporateInfoForm()
        return render(request,'Corporate/register.html',{'Corporate_form':Corporate_form,'Corporate_info_form':Corporate_info_form})
    
    def post(self,request):
        Corporate_form = CorporateForm(data=request.POST)
        Corporate_info_form = CorporateInfoForm(data=request.POST)
        email = request.POST['email']

        if Corporate_form.is_valid() and Corporate_info_form.is_valid():
            Corporate = Corporate_form.save()
            Corporate.set_password(Corporate.password)
            Corporate.is_active = True
            Corporate.is_staff = True
            Corporate.save()

            domain = get_current_site(request).domain
            email_subject = 'Activate your Varenyam Virtual Assessment Corporate account'
            email_body = "Hi. Please contact the admin team of "+domain+". To register yourself as a Trainer."+ ".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
            fromEmail = 'noreply@exam.com'
            email = EmailMessage(
				email_subject,
				email_body,
				fromEmail,
				[email],
            )
            Client_info = Corporate_info_form.save(commit=False)
            Client_info.user = Corporate
            if 'picture' in request.FILES:
                Client_info.picture = request.FILES['picture']
            Client_info.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            EmailThread(email).start()
            return redirect('Corporate-login')
        else:
            print(Corporate_form.errors,Corporate_info_form.errors)
            return render(request,'Corporate/register.html',{'Corporate_form':Corporate_form,'Corporate_info_form':Corporate_info_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'Corporate/login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']
		has_grp = False
		if username and password:
			user = auth.authenticate(username=username,password=password)
			exis = User.objects.filter(username=username).exists()
			if exis:
				user_ch = User.objects.get(username=username)
				has_grp = has_group(user_ch,"Trainer")
			if user and user.is_active and exis and has_grp:
				auth.login(request,user)
				messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")
				return redirect('Corporate-index')
			elif not has_grp and exis:
				messages.error(request,'You dont have permssions to login as Corporate. If You think this is a mistake please contact admin')	
				return render(request,'Corporate/login.html')
                
			else:
				messages.error(request,'Invalid credentials')	
				return render(request,'Corporate/login.html')
            
            

		messages.error(request,'Please fill all fields')
		return render(request,'faculty/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('faculty-login')