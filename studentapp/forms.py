from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']  # Fields to display in the form
      

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'state', 'zip_code', 'profile_picture']      

from django import forms
from .models import Room, Message

# Room form for creating rooms
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'image']

# Message form for sending messages
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
from django import forms
from django import forms
from .models import Course, CourseResource

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter course description'}),
        }

class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['course', 'name', 'description', 'resource_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter resource description'}),
        }

    # You can explicitly mark fields as required here
    # The fields are automatically required by default in Django forms unless explicitly set as optional.
    # If you want to customize the validation, you can adjust the 'required' parameter like below.

    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)
    resource_file = forms.FileField(required=True)
