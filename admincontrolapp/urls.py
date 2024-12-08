from django.urls import path
from . import views

app_name = 'admincontrolapp'

urlpatterns = [
    path('posts/', views.posts_view, name='posts'),  # Example view for posts
    # Add more URLs as needed for your admin control features
    path('unreport_post/<int:post_id>/', views.unreport_post, name='unreport_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
