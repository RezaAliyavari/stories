from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.conf import settings


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    


class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    is_active = models.BooleanField(default=False)  
    max_stories = models.PositiveIntegerField(default=0)  
    max_widgets = models.PositiveIntegerField(default=0)  
    stories_per_widget = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'


class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)#ایندکس
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE, db_index=True)#ایندکس
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.plan.title}'
    

class Widget(models.Model):

    SHAPE_CHOICE = [
        ('circle', 'CIRCLE'),
        ('square', 'SQUARE'),
        ('etc', 'ETC'),
    ]

    TITLE_CHOICE = [
        ('hidden', 'HIDDEN'),
        ('outside', 'outside'),
    ]

    ALIGN_CHOICE = [
        ('center', 'CENTER'),
        ('left', 'LEFT'),
        ('right', 'RIGHT'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    enable = models.BooleanField(default=True)
    shape = models.CharField(max_length=6, choices=SHAPE_CHOICE)
    title_position = models.CharField(max_length=7, choices=TITLE_CHOICE)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    align = models.CharField(max_length=6, choices=ALIGN_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Story(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)####uuid حذف
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    content = models.FileField(upload_to='story_contents/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey('Widget', related_name='stories', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.IntegerField(default=5)
    next_story = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, null=True, blank=True)
    previous_story = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} - {self.user.email}"


class DiscountCode(models.Model):
    TYPE_CHOICES = (
        ('percent', 'Percent'),
        ('price', 'Price'),
    )

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    value = models.IntegerField()
    max_use = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    GATEWAY_CHOICES = [
        ('shaparak', 'Shaparak'),
        ('zarinpal', 'Zarinpal'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)###
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)# ایندکس گذاری 
    discount_code = models.ForeignKey('DiscountCode', on_delete=models.SET_NULL, null=True, blank=True)#فارنگکی به مدل دیس کانت کد  و دیس کانت بیاد قبل این مدل 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    gateway = models.CharField(max_length=10, choices=GATEWAY_CHOICES)
    tracking_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} - {self.status}"


class Viewer(models.Model):
    viewer_session = models.UUIDField(default=uuid.uuid4, editable=False , unique=True, db_index=True)#ایندکس
    story = models.ForeignKey('Story', on_delete=models.CASCADE)
    os = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.viewer_session)
