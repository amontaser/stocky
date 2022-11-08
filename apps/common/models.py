import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from pkg_resources import require
from django.urls import reverse
from django.conf import settings

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, related_name='%(class)s_createdby')
    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, related_name='%(class)s_updatedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class BaseSoftDeletableModel(models.Model):
    is_deleted = models.BooleanField(default=False,blank=True)
    deleted_at = models.DateTimeField(null=True , blank=True)
    # deleted_by = models.ForeignKey(User, null=True,on_delete=models.CASCADE, blank=True,related_name="%(class)s_deleted_by")
    
    class Meta:
        abstract = True
        
    def soft_delete(self):
        self.is_deleted = True
        # self.deleted_by = user_id
        self.deleted_at = timezone.now()
        self.save()


