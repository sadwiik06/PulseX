from django.contrib import admin

# Register your models here.
# studentapp/admin.py
# studentapp/admin.py
from django.contrib import admin
from .models import Post, BlockedUser  

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_unsafe')

    def delete_model(self, request, obj):
        # Block the user by creating a BlockedUser  instance
        BlockedUser .objects.get_or_create(user=obj.user)
        
        # Call the parent class's delete method
        super().delete_model(request, obj)

admin.site.register(Post, PostAdmin)
admin.site.register(BlockedUser )