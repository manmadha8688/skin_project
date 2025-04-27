from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from app.models import PatientProfile

User = get_user_model() 


# Create your views here.
def register(request):
    if request.method == 'POST':
        
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken..!!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already used!!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,name=name,email=email)
                user.set_password(password1)
                user.save()
                profile = PatientProfile.objects.create(user=user,name=name,email=email)
                profile.save()
                return redirect('/accounts/login?registered=true')
        else:
            messages.info(request,'password not matching..')
            return redirect('register')


    return render(request,'accounts/register.html')

def login_view(request):
    if request.method == 'POST':

        username = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(request, 'Email not registered!')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.role=="doctor":
                return redirect('/doctor/?logged_in=true')

            return redirect('/patient?logged_in=true')
        else:
            messages.error(request,'Invalid Password!!!')
        
    return render(request,'accounts/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/patient?logged_out=true')

