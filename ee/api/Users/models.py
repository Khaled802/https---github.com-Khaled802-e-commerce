from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import re
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class Validation:
    
    def __init__(self, text) -> None:
        self.text = text
        self.length = len(text)

    def check_chars(self):
        if re.search('[a-z]', self.text) is None:
            return False
        if re.search('[A-Z]', self.text) is None:
            return False
        if re.search('[0-9]', self.text) is None:
            return False
        if re.search('\W', self.text) is None:
            return False
        return True

    def is_password(self) -> bool:
        if self.length <= 8:
            return False
        return self.check_chars()

    def is_email(self) -> bool:
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pattern, self.text):
            return True
        return False
        


class UserManager(BaseUserManager):
    @staticmethod
    def validate_info(email: str, password: str)-> None:
        email_valid = Validation(email).is_email()
        password_valid = Validation(password).is_password()
        
        if not email_valid:
            raise ValueError("Email is not correct")
        
        if not password_valid:
            return ValueError("Password is not valid")


    def create_user(self, email: str, password: str, **extra_fields):
        self.validate_info(email, password)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', "admin")
        extra_fields.setdefault('last_name', "admin")

        if not extra_fields.get("is_staff", False):
            raise ValueError('Superuser must have is_staff=True.')

        if not extra_fields.get("is_superuser", False):
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)
        


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self) -> str:
        return str(self.image)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)



    

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile_name', on_delete=models.CASCADE)
    picture = models.OneToOneField(ImageUpload, related_name='profile_picture', on_delete=models.CASCADE, null=True, blank=True,)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    code_country = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email


