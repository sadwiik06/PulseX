from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'student'
urlpatterns = [
    path('upload/', views.upload_post, name='upload_post'),
    path('posts/', views.posts_page, name='posts_page'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Add this line
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('search/', views.search_posts, name='search_posts'),
    path('room_list/', views.room_list, name='room_list'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'), 
    # In urls.py
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('courses/', views.course_management, name='course_management'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/upload/', views.upload_resources, name='upload_resources'),
    path('report_post/<int:post_id>/', views.report_post, name='report_post'),
    path('delete-account/', views.delete_account, name='delete_account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
