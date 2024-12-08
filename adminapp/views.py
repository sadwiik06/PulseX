from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

# Home page view
def home(request):
    return render(request, 'adminapp/home.html')

# About page view
def about(request):
    return render(request, 'adminapp/about.html')

# Contact Us page view

def contactus(request):
    if request.method == 'POST':
        # Your form handling logic here
        
        # After successful form submission:
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contactus')  # Redirect to the same or another page
    return render(request, 'adminapp/contactus.html')

# Services page view
def services(request):
    return render(request, 'adminapp/services.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'User registered successfully. Please login.')
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
    
    return render(request, 'adminapp/signup.html')


# Login view with username length check and redirection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username length is less than 5 characters
        if len(username) < 5:
            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)

            # Check if user exists and is an admin
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admincontrolapp:posts')  # Redirect to admin control posts page
            else:
                messages.error(request, 'Invalid username or password, or user is not an admin.')
                return render(request, 'adminapp/login.html')  # Render the login template with an error message

        # Username is valid, attempt to authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student:posts_page')  # Redirect to student posts page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/login.html')  # Render the login template again to display error

    return render(request, 'adminapp/login.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Send email view
def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Customize email body
        email_message = f"From: {name} <{email}>\n\n{message}"
        
        try:
            send_mail(
                subject=subject, 
                message=email_message, 
                from_email='saisadwiikkatam@gmail.com',  # Replace with your email
                recipient_list=['your_email@example.com'],  # Replace with your recipient email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'adminapp/contactus.html', {'success': True})  # Pass success flag to template
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'adminapp/contactus.html', {'success': False})  # Pass failure flag to template
    return render(request, 'adminapp/contactus.html')



# Logout view
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


# Student dashboard view (posts page)
def student_dashboard(request):
    return render(request, 'studentapp/posts.html')

# Debug view for displaying media settings
def debug_view(request):
    print("Debug view accessed") 
    return HttpResponse(f"MEDIA_URL: {settings.MEDIA_URL}, MEDIA_ROOT: {settings.MEDIA_ROOT}")
