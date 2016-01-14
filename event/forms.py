from .models import Event
from .models import Reservation
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from select_time_widget import *

class AddEvent(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('uid')        
        super(AddEvent, self).__init__(*args,**kwargs)
        self.fields['userid'].initial = uid
        
# day = forms.CharField(widget=forms.SelectDateWidget())
    
    start = forms.CharField(widget=forms.SelectDateWidget())
    end = forms.CharField(widget=forms.SelectDateWidget())
    userid = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Event
        fields = ['name','start','end','tags','userid']
        
class EditEvent(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        e = kwargs.pop('e')        
        super(EditEvent, self).__init__(*args,**kwargs)
        self.fields['userid'].initial = e.userid
        self.fields['name'].initial = e.name
        self.fields['start'].initial = e.start
        self.fields['end'].initial = e.end
        self.fields['tags'].initial = e.tags
        self.fields['id'].initial = e.id
        
    
    start = forms.CharField(widget=forms.SelectDateWidget())
    end = forms.CharField(widget=forms.SelectDateWidget())
    userid = forms.CharField(widget=forms.HiddenInput())
    id = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Event
        fields = ['name','start','end','tags','userid','id']    

        
class AddReservation(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        #if 'uid' in kwargs:
        uid = kwargs.pop('uid')        
        eid = kwargs.pop('eid')
        super(AddReservation, self).__init__(*args,**kwargs)
        self.fields['userid'].initial = uid
        self.fields['eventid'].initial = eid
    
    day = forms.CharField(widget=forms.SelectDateWidget())
    begin = forms.TimeField(widget=SelectTimeWidget(minute_step=30,twelve_hr=True,use_seconds=False))
    duration = forms.ChoiceField(choices=[(x,x) for x in range(1,24)])
    userid = forms.CharField(widget=forms.HiddenInput())
    eventid = forms.CharField(widget=forms.HiddenInput())
    #event_id = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Reservation
        fields = ['day','begin','duration','userid']
