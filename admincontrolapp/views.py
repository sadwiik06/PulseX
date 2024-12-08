# admincontrolapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When, Value, IntegerField
from studentapp.models import Post

def posts_view(request):
    if request.user.is_authenticated:
        print(f':User  {request.user.username}, Is Admin: {request.user.is_staff}')
    else:
        print('User  is not authenticated.')
        
    # Fetch posts ordered by reported status and then by creation date
    posts = Post.objects.annotate(
        reported_order=Case(
            When(is_unsafe=True, then=Value(0)),  # Reported posts come first
            When(is_unsafe=False, then=Value(1)),  # Unreported posts come next
            output_field=IntegerField(),
        )
    ).order_by('reported_order', '-created_at')  # Order by reported first, then by creation date

    return render(request, 'admincontrolapp/posts.html', {'posts': posts})

@csrf_exempt  # Use with caution; consider using CSRF tokens in production
def unreport_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            post.is_unsafe = False  # Assuming this is how you mark a post as unreported
            post.save()
            return JsonResponse({'success': True})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def delete_post(request, post_id):
    # Get the post object or return a 404 if it doesn't exist
    post = get_object_or_404(Post, id=post_id)

    # Delete the post
    post.delete()
   

    # Redirect to the posts list after deletion
    return redirect('admincontrolapp:posts')  # Corrected line # Adjust this to match your URL pattern