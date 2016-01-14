from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class AUser(models.Model):
    user = models.OneToOneField(User, null=True)
    
    def __str__(self):
        return self.user.username
    
