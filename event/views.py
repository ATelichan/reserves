from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
import pytz
from django.db.models import Max
from itertools import chain


from .models import Event
from .models import Reservation
from .forms import AddEvent
from .forms import AddReservation
from .forms import EditEvent
import logging

def index(request):
    allevents = Event.objects.order_by('-start')
    template = loader.get_template('event/index.html')
    context = {
        'allevents': allevents,
    }
    return HttpResponse(template.render(context, request))

def eventpage(request, eid):
    uid = None
    user = None
    if request.user.is_authenticated():
        uid = request.user.id
        user = request.user
        
    e = get_object_or_404(Event, pk=eid)
    
    if request.method == 'POST':
        add_reservation = AddReservation(uid=uid, eid=eid, data=request.POST)
        if add_reservation.is_valid():
            res = add_reservation.save(commit = False)
            rtime = res.begin
            pytz.timezone(timezone.get_default_timezone_name()).localize(rtime)
            
            if res.day >= e.start and res.day+timedelta(days=res.duration) <= e.end:
                res.event_id = eid
                res.save()
                e = get_object_or_404(Event, pk=eid)
                allres = Reservation.objects.filter(event_id=eid, day__gte = datetime.now()).order_by('day') #
                resform = AddReservation(uid=uid, eid=eid)
                context = {'user':user, 'event':e, 'add_reservation':resform,'allres':allres}
                if uid == e.userid:
                    edit_event = EditEvent(e=e)
                    context.update({'edit_event':edit_event})
                
                return render(request, 'event/eventpage.html', context) #
            else:
                return HttpResponse('reservatino outside of resource time range.')
           
        else:
            print add_reservation.errors
    elif uid == e.userid:
        e = get_object_or_404(Event, pk=eid)
        edit_event = EditEvent(e=e)
        add_reservation = AddReservation(uid=uid, eid=eid)
        allres = Reservation.objects.filter(event_id=eid, day__gte = datetime.now()) #
        return render(request, 'event/eventpage.html', {'user':user, 'event': e, 'add_reservation':add_reservation, 'allres':allres, 'edit_event':edit_event})
    else:
        e = get_object_or_404(Event, pk=eid)
        add_reservation = AddReservation(uid=uid, eid=eid)
        allres = Reservation.objects.filter(event_id=eid, day__gte = datetime.now()) #
        return render(request, 'event/eventpage.html', {'user':user, 'event': e, 'add_reservation':add_reservation, 'allres':allres})

def createevent(request):
    uid = None
    if request.user.is_authenticated():
       uid = request.user.id
        
    #context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        add_event = AddEvent(uid = uid, data=request.POST)
        
        if add_event.is_valid():
            event = add_event.save()
            event.save()
            registered = True
            return render(request, 'event/create.html')
        else:
             print add_event.errors
    else:
        add_event = AddEvent(uid = uid)
        #template = loader.get_template('homeland/register.html')
    
    return render(request, 'event/create.html', {'add_event': add_event})

def editevent(request,eid):
    uid = None
    if request.user.is_authenticated():
        uid = request.user.id
        user = request.user
    
    e = get_object_or_404(Event, pk=eid)
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        edit_event = EditEvent(e=e, data=request.POST, instance=e)
        
        if edit_event.is_valid():
            event = edit_event.save()
            event.save()
            registered = True
            allres = Reservation.objects.filter(event_id=eid, day__gte = datetime.now()).order_by('begin') #
            resform = AddReservation(uid=uid, eid=eid)
            context = {'user':user, 'event':e, 'add_reservation':resform,'allres':allres}
            if uid == e.userid:
                edit_event = EditEvent(e=e)
                context.update({'edit_event':edit_event})
            return render(request, 'event/eventpage.html', context) #

        else:
             print edit_event.errors
    else:
        return render(request, 'event')
    
def deletereservation(request, eid):
    r = get_object_or_404(Reservation, pk=eid).delete()
    uid = None
    if request.user.is_authenticated():
        user = request.user
    res = Reservation.objects.filter(userid = user.id, day__gte = datetime.now()) #
    events = Event.objects.filter(userid = user.id) #
    allevents = Event.objects.annotate(Max('reservation__pub_date')).order_by('-reservation__pub_date__max')
    context = {'user':user, 'myres':res, 'myevents':events,'allevents':allevents} #
    return render(request, 'homeland/home.html',context) #

def deleteevent(request, eid):
    r = get_object_or_404(Event, pk=eid).delete()
    uid = None
    if request.user.is_authenticated():
        user = request.user
    res = Reservation.objects.filter(userid = user.id, day__gte = datetime.now()) #
    events = Event.objects.filter(userid = user.id) #
    allevents = Event.objects.annotate(Max('reservation__pub_date')).order_by('-reservation__pub_date__max')
    context = {'user':user, 'myres':res, 'myevents':events,'allevents':allevents} #
    return render(request, 'homeland/home.html',context) #

def tags(request, tag):
    e = Event.objects.filter(tags__contains=tag)
    if e:
        return render(request, 'event/tags.html', {'e':e}) #
    else:
        return HttpResponse('nothign with this tag exists.')

def rss(request,eid):
    e = get_object_or_404(Event, pk=eid)
    allres = Reservation.objects.filter(event_id=eid) 
    
    return render(request,'event/rss.rss', {'e':e,'r':allres})
    
    