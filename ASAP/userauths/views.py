from django.shortcuts import render, redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method == 'POST': 
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully")
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user) 
                return redirect("core:index")
            else:
                messages.error(request, "Authentication failed. Please check your credentials.")
    else: 
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'userauths/signup.html',context)

def login_view(request):
    if request.user.is_authenticated: 
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try: 
            user = User.objects.all(email=email)

            if user is not None: 
                login(request, user)
                messages.success("You are Logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist. Create an account.")
        except:
            messages.warning(request, f"User with this {email} does not exist.")

        user = authenticate(request, email=email, password=password)
    
    
    context = {

    }

    return render(request, 'userauths/login.html', context)

def logout_view(request):
    logout(request)
    return redirect("userauths:sign-in")