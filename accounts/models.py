from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom User model with role-based permissions"""
    
    USER_ROLES = [
        ('client', 'Client'),
        ('artisan', 'Artisan'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='client',
        help_text='User role in the system'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the user account is verified'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def is_artisan(self):
        return self.role == 'artisan'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
