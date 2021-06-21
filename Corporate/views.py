
from django.shortcuts import render,redirect
from django.utils.http import urlsafe_base64_decode
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
from Client.utils import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.urls import reverse


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
            my_group = Group.objects.get_or_create(name='Corporate')
            my_group[0].user_set.add(Corporate)
            
            Corporate.save()
            uidb64 = urlsafe_base64_decode(force_bytes(Corporate.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(Corporate)})
            activate_url = 'http://' + domain +link
            email_subject = 'Activate your Varenyam Virtual Assessment Corporate account'
            email_body = "Hi. Please contact the admin team of "+domain+". To register yourself as a Trainer."+ activate_url+".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
            
            fromEmail = 'varenyamanalytics@gmail.com'
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
		return render(request,'Corporate/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('Corporate-login')


class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)

	
	def run(self):
		self.email.send(fail_silently = False)

class VerificationView(View):
	def get(self,request,uidb64,token):
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)
			if not account_activation_token.check_token(user,token):
				messages.error(request,"User already Activated. Please Proceed With Login")
				return redirect("Corporate-login")
			if user.is_active:
				return redirect('Corporate-login')
			user.is_active = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('Corporate-login')   