from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from core.utils import htmx_required
from django.contrib.auth import update_session_auth_hash
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from users.models import User
from urllib.parse import urlparse
from users.utils import is_last_url_named

# Create your views here.
def loginview(request):
 if request.user.is_authenticated:
        return redirect('index')
 else:
     if request.method == "POST":
        return manage_login(request)
     else:
        last_url = request.META.get('HTTP_REFERER')
        next_url = urlparse(last_url).path if is_last_url_named("detail_FBP2P", last_url) else None
        return render(request, 'users/login.html',{"next": next_url})

def manage_login(request):
         email = request.POST.get('email')
         password = request.POST.get('password')
         if (type(email) != str) or (len(email) > 60) or (type(password) != str):
             return HttpResponse('Invalid login data')
         user = authenticate(request, username=email, password=password)
         if user is None:
             if User.objects.filter(email__iexact=email).exists():
                    try:
                        username = User.objects.get(email__iexact=email).username
                        user = authenticate(username=username, password=password)
                    except:
                        user = None
         if user is not None:
             login(request, user)
             redirect_to = request.POST.get('next')
             if redirect_to != 'None':
                 return redirect(redirect_to)
             return redirect('index')
         else:
             messages.info(request, 'E-Mail, Benutzername oder Password falsch.')
             return render(request, 'users/login.html')

def logoutview(request):
 logout(request)
 return redirect('login')

def registerview(request):
 if request.user.is_authenticated:
        return redirect('index')
 else:
     form = CustomUserCreationForm()
     if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
             user = form.save()
             login(request, user)
             return redirect('/aufladen/?dialog')
         else:
             context = {'form': form}
             return render(request, 'users/register.html', context=context)
     return render(request, 'users/register.html')
 
@login_required
def settingsview(request):
  return render(request,'users/settings.html')

@login_required
def changemailview(request):
    if request.POST:
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, "Email erfolgreich geändert!")
        else:
            messages.error(request, "Email konnte nicht geändert werden.")
        return redirect('settings')


@login_required
def changepasswordview(request):
    if request.POST:
        pw_change_form = PasswordChangeForm(user=request.user,data=request.POST or None)
        if pw_change_form.is_valid():
            pw_change_form.save()
            update_session_auth_hash(request, pw_change_form.user) #not redirect to login
            messages.success(request,"Passwort erfolgreich geändert!")
        else:
            messages.error(request,"Passwort konnte nicht geändert werden.")
            #+ str(pw_change_form.errors.as_data())
        return redirect('settings')




