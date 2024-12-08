from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('contactus/', views.contactus, name='contactus'),  # Contact Us page
    path('services/', views.services, name='services'),  # Services page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),  # Signup page
     # Faculty page
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('debug/', views.debug_view, name='debug_view'), 
    path('send-email/', views.send_email, name='send_email'),
]
