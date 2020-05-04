from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, 'theplaza/register.html')
            else:
                user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name, email=email, password=password1)
                user.save()
                user = authenticate(username=username,password=password1)                   
                login(request, user)
                return redirect('/')

        else: 
            messages.info(request, "Passwords didnt matched")
            return render(request, 'theplaza/register.html')
    else:
        return render(request, 'theplaza/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
        else:
            messages.error(request, 'Username or Password is incorrect!', fail_silently=True)
            return render(request, 'theplaza/login.html')
    else:
        return render(request, 'theplaza/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect("ecommerce:home")


def PasswordChangeView(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    return render(request, 'theplaza/password_change_form.html', {'form':form})

class PasswordChangeDoneView():
    pass
