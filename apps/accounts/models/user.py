from email.policy import default
from django.contrib.auth.models import AbstractUser , BaseUserManager, AbstractBaseUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from apps.common.models import BaseModel
from django.conf import settings
import uuid
import avinit
import time

class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)
    superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    # notice the absence of a "Password field", that is built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Email & Password are required by default.

    def __str__(self):
        return self.username

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def get_absolute_url(self):
        # return reverse("users:user_detail", kwargs={"uuid": self.id})
        return reverse('users:user_detail', args=[str(self.id)]) 
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatar',null=True, blank=True,verbose_name=u"image (Recommended: 200X200)")
    language_code = models.CharField(
        max_length=35, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
    address  = models.TextField(blank=True, null=True)
    GENDER_CHOICES = ((1, 'Male'), (2, 'Female'))
    gender = models.IntegerField(choices=GENDER_CHOICES,null=True)
    language = models.CharField(_('Language'), choices=settings.LANGUAGES, max_length=7, default='en')
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    allow_login = models.BooleanField(default=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    password_salt = models.CharField(max_length=255, blank=True, null=True)
    password_reset_token = models.TextField(null=True, blank=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    is_login = models.IntegerField(default=False, null=False)

    def __str__(self):
        return self.user.username

    @ receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            try:
                Profile.objects.create(user=instance)
                name = instance.get_full_name()
                av = avinit.get_avatar_data_url(name)
                import base64
                imgdata = av.replace("data:image/svg+xml;base64,", "") + "=="
                imgdata = base64.b64decode(imgdata)
                url = "avatar/" + instance.username + str(time.time()) +".svg"
                filename = settings.MEDIA_ROOT+url
                with open(filename, 'wb') as f:
                    f.write(imgdata)
                instance.profile.image = url
                instance.profile.save()
            except ObjectDoesNotExist:
                Profile.objects.create(user=instance)
                instance.profile.save()

class UserGroupType(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    member_max = models.IntegerField(default=0)
    member_min = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class InGroup(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now_add=True)
    time_removed = models.DateTimeField(null=True, blank=True)
    group_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + " " + self.group.name
    
class UserGroup(BaseModel):
    user_group_type = models.ForeignKey(UserGroupType, on_delete=models.CASCADE)   
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user
# create super user with username
    def create_superuser(self,username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user