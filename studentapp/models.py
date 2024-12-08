from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect the post to a user
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Set a default image
    caption = models.TextField(max_length=500, blank=True)  # Post caption, optional
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post is created
    is_unsafe = models.BooleanField(default=False)  # Flag to mark the post as unsafe

    def __str__(self):
        return f'{self.user.username} - {self.caption[:30]}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='user.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.content[:30]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Ensure one user can like a post only once

    def __str__(self):
        return f"{self.user.username} likes {self.post.caption}"
    
from django.db import models
from django.contrib.auth.models import User

# Room model
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Message model
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"

# models.pyfrom django.db import models

from django.db import models
from django.core.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name



class CourseResource(models.Model):
    course = models.ForeignKey(Course, related_name='resources', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    resource_file = models.FileField(upload_to='course_resources/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'name')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Course: {self.course.name})"

    @property
    def download_url(self):
        if self.resource_file and hasattr(self.resource_file, 'url'):
            return self.resource_file.url
        return ''


class BlockedUser (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email