from django.shortcuts import render, redirect
from .models import ClientPreferenceModel
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    exists = ClientPreferenceModel.objects.filter(user=request.user).exists()
    Client_preference = None
    
    if request.method == 'GET':
        var = "On"
        if exists:
            var="Off"
            Client_preference = ClientPreferenceModel.objects.get(user=request.user)
            if Client_preference.sendEmailOnLogin == True:
                var = "On"
        return render(request,'ClientPreferences/pref.html',{'Client_preference':Client_preference,'email_pref_value':var})

    if request.method == 'POST':
        if exists:
            Client_preference = ClientPreferenceModel.objects.get(user=request.user)
            var = "Off"
        pref = request.POST['email_pref']
        if exists:
            Client_preference.sendEmailOnLogin = pref
            Client_preference.save()
        else:
            var = "On"
            ClientPreferenceModel.objects.create(user = request.user, sendEmailOnLogin=pref)

        Client_preference = ClientPreferenceModel.objects.filter(user=request.user)
        if pref == 'True':
            var = "On"

        messages.success(request,"Email Notifications are turned " + var)

        return render(request,'ClientPreferences/pref.html',{'Client_preference':Client_preference,'email_pref_value':var})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ClientPreferences/change_password.html', {
        'form': form
    })