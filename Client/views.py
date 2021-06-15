from django.shortcuts import render,redirect
from django.views import View
from .forms import ClientForm, ClientInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.models import User
from ClientPreferences.models import ClientPreferenceModel
from django.contrib.auth.models import Group

@login_required(login_url='login')
def index(request):
    return render(request,'Client/index.html')

class Register(View):
    def get(self,request):
        Client_form = ClientForm()
        Client_info_form = ClientInfoForm()
        return render(request,'Client/register.html',{'Client_form':Client_form,'Client_info_form':Client_info_form})
    
    def post(self,request):
        Client_form = ClientForm(data=request.POST)
        Client_info_form = ClientInfoForm(data=request.POST)
        email = request.POST['email']

        if Client_form.is_valid() and Client_info_form.is_valid():
            Client = Client_form.save()
            Client.set_password(Client.password)
            Client.is_active = False
            my_group = Group.objects.get_or_create(name='Client')
            my_group[0].user_set.add(Client)
            Client.save()

            uidb64 = urlsafe_base64_encode(force_bytes(Client.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(Client)})
            activate_url = 'http://' + domain +link
            email_subject = 'Activate your Varenyam Virtual Assessment Portal account'
            email_body = 'Hi.Please use this link to verify your account\n' + activate_url + ".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
            fromEmail = 'Varenyamanalytics@gmail.com'
            email = EmailMessage(
				email_subject,
				email_body,
				fromEmail,
				[email],
            )
            Client_info = Client_info_form.save(commit=False)
            Client_info.user = Client
            if 'picture' in request.FILES:
                Client_info.picture = request.FILES['picture']
            Client_info.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            EmailThread(email).start()
            return redirect('login')
        else:
            print(Client_form.errors,Client_info_form.errors)
            return render(request,'Client/register.html',{'Client_form':Client_form,'Client_info_form':Client_info_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'Client\login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']

		if username and password:
			exis = User.objects.filter(username=username).exists()
			if exis:
				user_ch = User.objects.get(username=username)
				if user_ch.is_staff:
					messages.error(request,"You are trying to login as User, but you have registered as Corporate USer. We are redirecting you to faculty login. If you are having problem in logging in please reset password or contact admin")
					return redirect('Corporate-login')
			user = auth.authenticate(username=username,password=password)
			if user:
				if user.is_active:
					auth.login(request,user)
					Client_pref = ClientPreferenceModel.objects.filter(user = request.user).exists()
					email = User.objects.get(username=username).email

					email_subject = 'You Logged into your Varenyam Virtual Assessment account'
					email_body = "If you think someone else logged in. Please contact support or reset your password.\n\nYou are receving this message because you have enabled login email notifications in portal settings. If you don't want to recieve such emails in future please turn the login email notifications off in settings."
					fromEmail = 'noreply@exam.com'
					email = EmailMessage(
						email_subject,
						email_body,
						fromEmail,
						[email],
					)
					if Client_pref :
						Client = ClientPreferenceModel.objects.get(user=request.user)
						sendEmail = Client.sendEmailOnLogin 
					if not Client_pref :
						EmailThread(email).start()
					elif sendEmail:
						EmailThread(email).start()
					messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")

					return redirect('index')
			
			else:
				user_n = User.objects.filter(username=username).exists()
				if user_n:
					user_v = User.objects.get(username=username)
					if user_v.is_active:
						messages.error(request,'Invalid credentials')	
						return render(request,'Client/login.html')
					else:
						messages.error(request,'Account not Activated')
						return render(request,'Client/login.html')

		messages.error(request,'Please fill all fields')
		return render(request,'Client/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')

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
				return redirect("login")
			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('login')
	
