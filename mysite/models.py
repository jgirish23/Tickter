from django.db import models
import uuid
# Create your models here.

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Username = models.CharField(max_length=255,blank=False)
    Title = models.CharField(max_length=255,blank=False)
    Description = models.TextField(max_length=255)
    Email = models.EmailField(max_length=254, blank=False)
    file= models.FileField(blank=True, null=True)
    Time = models.DateTimeField(auto_now=True)
    Status = models.BooleanField(default=False, blank=False)





