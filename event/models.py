#from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
   
import datetime
from datetime import datetime

class Event(models.Model):
    name = models.CharField(max_length=200)
    userid = models.IntegerField(default=0)
    start = models.DateField(default=datetime.today)
    end = models.DateField(default=datetime.today)
    tags = models.CharField(max_length=250, null=True)
    pub_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.name
    
    def gettags(self):
        return self.tags.split(',')
    
#    def duration(self):
#        return end-start;


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    userid = models.IntegerField(default=0)
    day = models.DateField(default=datetime.today)
    begin = models.TimeField()
    duration = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.event.name
    
    def name(self):
        return self.event.name
    
    def getusername(self):
        try:
            return User.objects.get(id=self.userid).username
        except User.DoesNotExist:
            return 'unknown'
        
    def getuserid(self):
        try:
            return self.userid
        except User.DoesNotExist:
            return 'unknown'