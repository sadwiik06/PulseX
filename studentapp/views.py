from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Like, Post, Comment
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post  # Added Post to the import

# View for uploading a new post

from django.contrib import messages


HARMFUL_KEYWORDS = [
    # General offensive terms
    'spam', 'violence', 'hate', 'abuse', 'harassment', 'offensive', 
    'insult', 'bullying', 'threat', 'slur', 'obscenity', 

    # Specific threats or harmful intents
    'kill', 'murder', 'attack', 'assault', 'rape', 'suicide', 'self-harm',
    'terrorism', 'bomb', 'shoot', 'arson', 'explosive',

    # Discriminatory or hateful phrases
    'racist', 'sexist', 'homophobic', 'transphobic', 'misogyny', 
    'bigotry', 'xenophobia', 'religious intolerance', 

    # Cyberbullying or trolling
    'doxxing', 'leaking personal info', 'revenge', 'hate speech', 
    'cyberstalking', 'troll', 'hateful', 'abusive language',

    # Profanity or vulgar language (examples - extend as needed)
    'f***', 's***', 'b****', 'c***', 'a******',

    # Sexual or explicit content
    'porn', 'explicit', 'sexual harassment', 'nudity', 'non-consensual', 
    'child exploitation', 'pedophilia',

    # Harmful behaviors or encouragement
    'drink bleach', 'harm yourself', 'end it all', 'jump off', 
    'take pills', 'die', 'encouraging harm', 'you’re worthless',

    # Phishing, scams, or fraud
    'win money', 'lottery', 'prize', 'click this', 'send money', 
    'bank details', 'phishing', 'fraudulent',

    # Commonly flagged hate-related phrases
    'go back to your country', 'you people are', 'you’re disgusting', 
    'nobody likes you', 'you’re a mistake', 'you don’t belong',

    # Misinformation or dangerous advice
    'fake news', 'vaccines are poison', 'earth is flat', 'dangerous advice', 
    'deny holocaust', 'spread lies', 'false claims',

    # Additional harmful phrases (extend as per need)
    'nobody loves you', 'world would be better without you', 
    'just do it (in self-harm context)', 'kill yourself', 'worthless', 
    'you’re ugly', 'nobody cares', 'why are you alive'
]

# studentapp/views.py
from django.shortcuts import render, redirect
from .models import Post, BlockedUser  
from .forms import PostForm  # Make sure you have a PostForm defined
from django.contrib import messages

# Define harmful keywords

def upload_post(request):
    # Check if the user is blocked
    if BlockedUser .objects.filter(user=request.user).exists():
        messages.error(request, 'You are blocked from uploading posts.')
        return render(request, 'studentapp/upload_post.html', {'form': PostForm()})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user
            
            # Check if the caption contains harmful keywords
            caption = post.caption.lower()  # Assuming your model has a caption field
            if any(keyword in caption for keyword in HARMFUL_KEYWORDS):
                # Block the user by creating a BlockedUser  instance
                BlockedUser .objects.get_or_create(user=request.user)
                
                # Show an alert message
                messages.error(request, 'Your post contains harmful content and you have been blocked from uploading further posts.')
                return redirect('student:posts_page')  # Redirect to the posts page or wherever you want

            post.save()
            messages.success(request, 'Your post has been uploaded successfully.')
            return redirect('student:posts_page')  # Redirect to the posts page
    else:
        form = PostForm()
    
    return render(request, 'studentapp/upload_post.html', {'form': form})




# View for displaying posts
def posts_page(request):
    posts = Post.objects.all().order_by('-created_at')
    # Remove the line that's causing the error
    # No need to manually fetch comments, Django will handle this through the related_name
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()
        print(f"Post ID: {post.id}, Is Unsafe: {post.is_unsafe}")
    return render(request, 'studentapp/posts.html', {'posts': posts})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the general profile information form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if 'profile_picture' in request.FILES:
            # Handle the profile picture upload
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if p_form.is_valid():
                p_form.save()
                return redirect('student:profile_edit')

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('student:profile_edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'studentapp/profile_edit.html', context)

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('student:posts_page')  # Redirect back to the posts page

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect(reverse('student:posts_page')) # Redirect back to the posts page

def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:  # If the like already exists, remove it
            like.delete()
            liked = False
        else:  # If it was a new like
            liked = True
            
        like_count = post.likes.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})

    return redirect('student:posts_page') 
     # Redirect after POST
from django.shortcuts import render
from .models import Post  # Import your Post model

def search_posts(request):
    username = request.GET.get('username')
    if username:
        posts = Post.objects.filter(user__username__icontains=username)  # Adjust according to your Post model
    else:
        posts = Post.objects.none()  # No posts if no username is provided

    return render(request, 'your_template_name.html', {'posts': posts})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Message
from .forms import RoomForm, MessageForm

# Room list view: List rooms and create new rooms
def room_list(request):
    rooms = Room.objects.all()

    # Handle form submission to create a new room
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student:room_list')
    else:
        form = RoomForm()

    return render(request, 'studentapp/rooms.html', {'rooms': rooms, 'form': form})


# Room detail view: Show messages in a room
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.all()

    # Handle form submission to send a message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.author = request.user
            message.save()
            return redirect('student:room_detail', room_id=room.id)
    else:
        form = MessageForm()

    return render(request, 'studentapp/room_detail.html', {'room': room, 'messages': messages, 'form': form})

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import Profile

# In views.py
def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'studentapp/profile.html', {'profile': profile})
from django.shortcuts import render, redirect
from .models import Course, CourseResource
from .forms import CourseForm, CourseResourceForm

from django.shortcuts import render, redirect
from .models import Course, CourseResource
from .forms import CourseForm, CourseResourceForm

def create_course(request):
    if request.method == 'POST':
        form_course = CourseForm(request.POST)
        if form_course.is_valid():
            form_course.save()
            return redirect('student:course_management')  # Use the namespace here
    else:
        form_course = CourseForm()

    return render(request, 'studentapp/create_course.html', {
        'form_course': form_course,
    })

def create_course(request):
    if request.method == 'POST':
        form_course = CourseForm(request.POST)
        if form_course.is_valid():
            form_course.save()
            return redirect('course_management')  # Redirect to the course management page
        else:
            print("Course form errors:", form_course.errors)  # Debugging line
    else:
        form_course = CourseForm()

    return render(request, 'studentapp/create_course.html', {
        'form_course': form_course,
    })

def upload_resources(request):
    resources = CourseResource.objects.all()

    if request.method == 'POST':
        form_resource = CourseResourceForm(request.POST, request.FILES)
        if form_resource.is_valid():
            # Ensure a course is selected
            if form_resource.cleaned_data['course']:
                form_resource.save()
                return redirect('course_management')  # Redirect to the course management page
            else:
                form_resource.add_error('course', 'Please select a course.')
        else:
            print("Resource form errors:", form_resource.errors)  # Debugging line
    else:
        form_resource = CourseResourceForm()

    return render(request, 'studentapp/upload_resources.html', {
        'form_resource': form_resource,
        'resources': resources,
    })
# studentapp/views.py
from django.shortcuts import render

def course_management(request):
    # Your view logic here
    return render(request, 'studentapp/course_management.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post

@login_required
def report_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # Check if the post has already been reported
        if not post.is_unsafe:
            post.is_unsafe = True
            post.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Post has been reported as unsafe.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Post already reported.'
            })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method. Use POST to report a post.'
    })

# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages

User  = get_user_model()

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to a suitable page after deletion

    return render(request, 'studentapp/delete_account.html')