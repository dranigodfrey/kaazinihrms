from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have email!')
        user = self.model(
            email  = self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_ROLES = (
        ('admin', 'Admin'),
        ('hr_admin', 'HR Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
 
    SEX = (
        ('male', 'Male'),
        ('female','Female'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length = 30)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20,  blank=True, null=True)
    second_name = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, choices=SEX, blank=False, default='Male')
    user_role = models.CharField(choices=USER_ROLES, blank=False,  default='Supervisee')
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    last_login = models.DateTimeField(auto_now_add = True)
    date_joined = models.DateField(auto_now = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
