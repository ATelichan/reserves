from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from datetime import datetime
from django.db.models import Max
from itertools import chain
from django.contrib.auth.models import User

from .models import AUser
from .forms import UserForm
from event.models import Reservation #
from event.models import Event #


def index(request):
    template = loader.get_template('homeland/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def loginuser(request):
    context = RequestContext(request)
    if(request.method == 'POST'):
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                res = Reservation.objects.filter(userid = user.id, day__gte = datetime.now()).order_by('day') #
                events = Event.objects.filter(userid = user.id) #
                eventsreserved = Event.objects.filter(reservation__isnull=False).annotate(Max('reservation__pub_date')).order_by('-reservation__pub_date__max')
                eventsnonreserved = Event.objects.filter(reservation__isnull=True)
                allevents = list(chain(eventsreserved,eventsnonreserved))
               
                context = {'user':user, 'myres':res, 'myevents':events,'allevents':allevents} #
                return render(request, 'homeland/home.html',context) #
            else:
                return HttpResponse("Not active")
        else:
            print "Invalid details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid details.")
    else:
        uid = None
        if request.user.is_authenticated():
            user = request.user
        res = Reservation.objects.filter(userid = user.id, day__gte = datetime.now()) #
        events = Event.objects.filter(userid = user.id) #
        allevents = Event.objects.annotate(Max('reservation__pub_date')).order_by('-reservation__pub_date__max')
        context = {'user':user, 'myres':res, 'myevents':events,'allevents':allevents} #
        return render(request, 'homeland/home.html',context) #
        #template = loader.get_template('homeland/home.html')
        #return HttpResponse(template.render(context, request))
        #return render(request, 'homeland/home.html',{'user':user})


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            user_form = UserForm()
            return render(request, 'homeland/register.html',{'user':user})
        else:
             print user_form.errors
    else:
        user_form = UserForm()
    return render(request, 'homeland/register.html', {'user_form': user_form})

def userpage(request,uid):
    try:
        user = User.objects.get(id=uid)
        res = Reservation.objects.filter(userid = uid, day__gte = datetime.now()).order_by('day') #
        events = Event.objects.filter(userid = uid) #
        eventsreserved = Event.objects.filter(reservation__isnull=False).annotate(Max('reservation__pub_date')).order_by('-reservation__pub_date__max')
        eventsnonreserved = Event.objects.filter(reservation__isnull=True)
        allevents = list(chain(eventsreserved,eventsnonreserved))
               
        context = {'user':user, 'myres':res, 'myevents':events,'allevents':allevents} #
        return render(request, 'homeland/user.html',context) #
    except User.DoesNotExist:
        return HttpRequest('No User here')


@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect('/')

