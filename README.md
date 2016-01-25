# reserves

Andrew Telichan-Phillips
Open Source Tools
Fall 2015
Final Project Documentation


Application Features
The functioning application can be found at the following URL: 
-https://fierce-bastion-1145.herokuapp.com/

The system supports multiple users, where each user can create their own resources and reserve them.  The following app features are generally described in order of the instructions for the assignment.

Once you reach the URL, you must register your username and password.  Once accomplished, you can sign in to a homepage where you will see (1) reservations made for resources by the user, sorted by time, (2) all resources in the system, in reverse order from the last reservation made, (3) resources the user owns, each linked to its own URL, and (4) a link to create a new resource.

When a resource is created, one can view (1) the name of the resource, (2) available hours for reservations, (3) and any tags that describe the type of resource. 

Once end time for a reservation has passed, it will not be shown anymore.

Each resource provides a URL that can be used to (1) show the current and upcoming reservations for a resource (depends on times owner specified as possible for reservation), (2) add a new reservation for the resource, and (3) edit information about the resource.  This is possible only if the user viewing the resource is the owner. When editing, the previously entered information about the resource is shown in the form as default values. Anywhere else a resource name is shown, it links to the corresponding URL.

Start times and durations resources can be specified. If you try to make a reservation when a resource is not available, or is not within the available hours, the interface will not accept the reservation and explains why – e.g., “reservation outside of resource time range.”

Each reservation displays the user, resource name, reservation time and duration. The resource name is linked to the resource page, and the user is linked to a page that shows all the reservations and resources for a user.

Existing reservations can be deleted by the user who made the reservation. 

Each resource supports the addition of tags (res. When creating or editing a resource, the owner can specify 0 or more tags. When viewing resources, the tags for the resource will be shown, and each tag links to a URL that shows all the resources with the given tag.

Finally, each resource has an RSS link that dumps all reservations for the resource in XML format: e.g., All Reservations for reunion Jan. 20, 2016, 10:17 p.m. 1800 reservation by ATelichan for 1 on Jan. 28, 2016 starting at 1 a.m. Jan. 20, 2016, 10:17 p.m.


Source
Source Code is available in the following GitHub repository (with one branch representing a version in which event IDs are eliminated, tagged “experiment”):
https://github.com/ATelichan/reserves.git


Developer Information
This project was created using Django. It is written in Python 2.7.11 and was deployed using Heroku Cloud Application Platform.

There are two Django apps included: the first, “homeland,” handles the home page, user creation, login, and user views. The second, “event,” handles the creation, displaying, editing, and deleting of the resources and reservations. 

Model Forms are used, and when appropriate, form data is sent back to the same view and template from which it originated. Since the development was focused on creating a functional interface, only basic HTML markup was used. 

Two open source third party widgets are used (“SelectTimeWidget” and “select_time_widget” to simplify the input of date and time objects.

To address the functionality of the code in greater detail, we will go through the steps required to establish user registration, as well as event and reservation creation, referring to specific files and lines of code.


Homeland App:
Upon visiting the URL, the system looks at urls.py in main reserves folder.  Inside this doc are a series of potential URL structures that could come in using regular expressions and “include” statements.  If this structure of the particular URL is called, then a URL structure is set up in the homeland app folder.

Inside the homeland app, the file homeland → urls.py loads a particular view by calling a function that is defined in views.py file (e.g., “loginuser,” which includes a set of instructions that handles the creation of new users and their IDs, as well as subsequent log-in capabilities).  The system then runs through that particular function and sends user information to the template file located in the folder: homelands —> templates —> homeland —> index.html.  User information is sent to the html file and rendered to the browser window.

Returning to homeland → views.py, line 30, a “request.method” is used to look at the URL, and if a post is made, then the user form data was sent (the method checks data against Django’s native user model in order to make sure the information matches, then loads the appropriate HTML file).  User, Event, and Reservation data are then pulled from the database and are added to the dictionary variable “context,” which ensures that results are sent to template files, so that the HTML file(s) can render with the appropriate information.

Lines 18-19 include models from within the event app, which contain the frameworks for the creation of objects that deal with event and reservation creation and storage.  


Event App:
Looking again at the login function in homeland —> views.py: this file gets all event objects from database, then filters them so we only get event objects where an event id is attached to a user id, based on who is currently logged in.  A chunk of code will be discussed line-by-line to illustrate how database information is handled and rendered using the file models.py in the event app, and the methods of classes defined within.

Starting in App homeland → views.py:
-Line 39 filters the information, confirms when a reservation is made, and then orders the reservation by nearest date (see folder/file/class in event → models.py → “class Reservation”).
-Line 40 finds all events that are created by user (here referring to the Event class in event → models.py).  
-Line 41 gets all events, organized by most recent reservation, ordered by earliest date (“filter(reservation__isnull=False)” is called if there is a existing reservation.
-Line 42 finds all events where there are no reservations
-Line 43 puts together a list of both events where reservations have and have not yet been made
-Line 45 another dictionary variable called “context” is created with all information from previous lines
-Line 46 looks at homeland home.html and renders that template

In homeland → templates → homeland → home.html: 
-Line 20, if the user is authenticated, the file is rendered, creating relevant buttons and other user interface elements 
-Line 27 executes all commands up to line 35, rendering everything stored in “myres” (from the dictionary variable “context” in homeland → views.py)
-Line 32 – “{% if user.id == reservation.userid %}” – checks if the current logged-in user was the creator of a reservation, in which case they are able to delete it, if so desired

Back to App homeland → views.py → “register (request)” (line 66): 
-Line 67 checks on whether a user is registered, and if not registered, a UserForm is created (line 82)

In App event —> views.py → “createevent(request)” (line 77): 
This function creates an event, checks if user is there, and creates a user ID.
-Line 94 checks if the appropriate form has been sent, and if not, adds an event (line 95) 

In event → forms.py
-Line 9 contains the AddEvent class
-Lines 18-20 create the form inputs, defining particular types of inputs (calling widgets — based on the following models: https://github.com/antihero/django-select-time-widget & https://www.djangosnippets.org/snippets/1202/)
-Line 11, once the event is added, the “init” function is run, which gets passed any variable sent to the function as kwargs
-Line 14 sets field user ID to ID that was passed from homeland → views.py
-Line 22 contains a Meta class, which tells Django that the created form is dealing with an event, along with fields to use from the event model (defined in event —> models —> models.py)

In App event → views.py 
-Line 95 finds the AddEvent form
-Line 98 sends the form to event → templates → create.html,  and is submitted

From MAIN folder reserves → reserves —> urls.py 
-Line 21 adds the event to the URL (???)

In App event → urls.py 
Line 15 matches information to that entered in event → views.py → “createevent”

In App event —> views.py 
-Lines 84-85, AddEvent gets passed the current user id, plus information that came from the posting of the form
-Line 87 checks to make sure the form is valid (there are no default values, so specific types of information are required, and errors are flagged if not provided — established in event → models.py)
-Line 89 saves the event and adds associated form data into the database

To event → templates → event → create.html with no context 
-The request method in views.py is set to “POST,” and create.html declares “Success!” and returns user to login screen

The remainder of this code operates in a very similar flow of information as described above, the standard Django workflow.  The URL that is sent to the browser is parsed by the urls.py files in order to call the appropriate views.py function. In the views.py function, data is gathered from the databases, parsed, and passed to the corresponding html template. The template renders HTML to the browser with the information that was passed from the views.py function.

 


