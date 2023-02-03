from django.contrib import admin
from .models import User, UserProfile, ImageUpload
# Register your models here.
class ImageUploadAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User)
admin.site.register(ImageUpload, ImageUploadAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

