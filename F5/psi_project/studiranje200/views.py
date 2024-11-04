#Created by: 
#   Vanja Tomic 0289/21
#   Konstantin Vuckovic 0524/21
#   Vladimir Bogojevic 0387/21
#   Mihajlo Antonijevic 0382/21

import json
import re
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import time
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.db.models import Count, Q, F, ExpressionWrapper, IntegerField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .templatetags.filters import mutual_conns

# Create your views here.

###########################################################################################################################################
# Decorators
###########################################################################################################################################



def remove_file_path_decorator(view_func):
    """
    A decorator function that removes the file path from the session.

    This decorator is intended to be used with views that handle GET requests.
    It removes the file path stored in the session, if it exists.

    Parameters:
    - view_func (function): The view function to be decorated.

    Returns:
    - function: The decorated view function.

    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'GET':
            file = request.session.pop('file_path', None)
            if file:
                pass
                #os.remove(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file)))
        return view_func(request, *args, **kwargs)
    return _wrapped_view



###########################################################################################################################################
# Event Views
###########################################################################################################################################



@login_required
@require_POST
def create_review(request, event_id):
    """
    Create a review for an individual :model:`main.Event`.

    **Parameters**

    ``request``
        The request object.

    ``event_id``
        The ID of the :model:`main.Event` for which the review is being created.

    **Post Parameters**

    ``comment``
        The comment text for the review.

    ``rating``
        The rating for the review.

    **Redirects to:**

    :view:`main.event_details`
    """
    event = Event.objects.get(id=event_id)
    comment = request.POST.get('comment')
    rating = request.POST.get('rating')

    if comment and rating:
        EventReview.objects.create(
            event=event,
            user=request.user,
            comment=comment,
            rating=rating,
            created_at=timezone.now()
        )

    return redirect('event_details', event_id=event_id)

@remove_file_path_decorator
def events(request):
    """
    Display a list of events.

    **Parameters**

    ``request``
        The HTTP request object.

    **Context**

    ``events``
        A QuerySet of :model:`main.Event` instances.

    ``places``
        A QuerySet of :model:`main.Place` instances.

    ``page``
        A string representing the current page.

    ``participations``
        A QuerySet of :model:`main.EventParticipation` instances related to the current user.

    **Template**

    :template:`front/events.html`
    """
    today = timezone.now().date()
    try:
        event_p = request.user.event_participations.all()
    except:
        event_p = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'filter':
            eventType = request.POST.get('type')
            datefrom = request.POST.get('datefrom')
            dateto = request.POST.get('dateto')
            datefrom = datetime.strptime(datefrom, '%Y-%m-%d').date()
            dateto = datetime.strptime(dateto, '%Y-%m-%d').date()
            places = Place.objects.all()
            eventTypes = EventType.objects.all()

            if eventType != "category" and datefrom and dateto:
                events = Event.objects.filter(event_type__name=eventType, date__range=[datefrom, dateto])
            else:
                events = Event.objects.filter(date__range=[datefrom, dateto])

            return render(request, 'front/events.html', {'events': events, 'page': "events", 'places': places,
                                                         'datefrom': datefrom.strftime('%Y-%m-%d'),
                                                         'dateto': dateto.strftime('%Y-%m-%d'), 'eventType': eventType,
                                                         'eventTypes': eventTypes,
                                                         'participations': event_p, 'today': today})

        # Retrieve fields from form
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        event_type = request.POST.get('type')
        place_id = request.POST.get('place')
        user_id = request.user.id
        # organization = Organization.objects.get(org_id=1)
        organization = OrganizationUser.objects.get(user_id=user_id, role="member").org
        place = Place.objects.get(place_id=place_id)
        # Handle date
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time2 = datetime.strptime(time_str, '%H:%M').time()

        # organizationuser = OrganizationUser(user=request.user, org=organization, role='admin', join_date=datetime.now())
        # organizationuser.save()

        # Create new event
        if title and description and date and time_str and time2:  # Basic validation
            event = Event(
                name=title,
                description=description,
                date=date,
                time=time2,
                org=organization,
                status='Published',
                event_type=EventType.objects.filter(name=event_type).first(),
                created_at=datetime.now(),
                total_rating=0,
                count_rating=0,
                place=place
            )
            event.save()
            file_path = request.session.pop('file_path', None)
            if file_path:
                with open(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)), 'rb') as f:
                    event.picture = File(f, name=str(time.time()) + '.jpg')
                    event.save()
                os.remove(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)))
            else:
                event.picture = File(open('static/images/avatar/placeholder.jpg', 'rb'), name=str(time.time()) + '.jpg')
                event.save()
            # sending notifications to followers
            followers_temp = OrganizationUser.objects.filter(org=organization, role='follower')

            # To get the actual User200 instances of these followers
            followers = [org_user.user for org_user in followers_temp]

            notification_type = NotificationType.objects.get(id=7)
            notifications = []
            for follower in followers:
                notification = Notification(
                    user=follower,
                    from_id=organization.org_id,
                    from_type='organization',
                    message=f"{title}",
                    notification_type=notification_type,
                    status='unread',
                    created_at=timezone.now()
                )
                notifications.append(notification)

            # Bulk create notifications
            Notification.objects.bulk_create(notifications)

            return redirect('events')  # Redirect after POST
        else:
            print("ERROR")

    # Retrieve all events from the database
    events = Event.objects.filter(date__gt=datetime.now().date())
    places = Place.objects.all()
    datefrom = datetime.now().date().strftime('%Y-%m-%d')
    dateto = datetime.now().date().strftime('%Y-%m-%d')
    eventTypes = EventType.objects.all()
    # Render a template with the list of events
    return render(request, 'front/events.html',
                  {'events': events, 'page': "events", 'places': places, 'datefrom': datefrom, 'dateto': dateto,
                   'eventType': "category", 'eventTypes': eventTypes, 'participations': event_p, 'today': today})

def event_details(request, event_id):
    """
    Display the details of an individual :model:`main.Event`.

    **Parameters**

    ``request``
        The request object.

    ``event_id``
        The ID of the :model:`main.Event` whose details are to be displayed.

    **Context**

    ``event``
        An instance of :model:`main.Event`.

    ``page``
        A string representing the current page.

    ``similar_by_place``
        A QuerySet of :model:`main.Event` instances that are similar to the current event by place.

    ``similar_by_organization``
        A QuerySet of :model:`main.Event` instances that are similar to the current event by organization.

    ``event_reviews``
        A QuerySet of :model:`main.EventReview` instances related to the current event.

    ``today``
        The current date.

    ``participations``
        A QuerySet of :model:`main.EventParticipation` instances related to the current user.

    ``users_in_event``
        A QuerySet of :model:`main.User200` instances participating in the current event.

    ``event_user`` (optional)
        An instance of :model:`main.EventUser` related to the current user and event. This is only included in the context if the user is authenticated.

    **Template:**

    :template:`front/event-details.html`

    **Form Parameters**

    ``comment``
        The comment text for the review.

    ``rating``
        The rating for the review.
    """
    event = Event.objects.get(event_id=event_id)
    similar_by_place = Event.objects.filter(place=event.place).exclude(event_id=event_id)[:3]
    similar_by_organization = Event.objects.filter(org=event.org).exclude(event_id=event_id)[:3]
    event_reviews = EventReview.objects.filter(event=event)
    if (request.user.is_authenticated):
        event_user = EventUser.objects.filter(user=request.user, event=event, status='interested').first()
    today = timezone.now().date()

    try:
        event_p = request.user.event_participations.all()
    except:
        event_p = None


    event_users = EventUser.objects.filter(event=event)
    users_event = User200.objects.filter(eventuser__in=event_users)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if rating is None:
            rating = 0
        else:
            rating = int(rating)

        if comment:
            EventReview.objects.create(
                event=event,
                user=request.user,
                comment=comment,
                created_at=timezone.now()
            ).save()
            if event_user.rating == None:
                event_user.rating = rating
                event_user.save()
                event.total_rating += rating
                event.count_rating += 1
                event.save()
                location = event.place
                location.total_rating += rating
                location.count_rating += 1
                location.save()
                org = event.org
                org.total_rating += rating
                org.count_rating += 1
                org.save()

        # Redirect to avoid re-submitting the form on page refresh
        return HttpResponseRedirect(reverse('event_details', args=[event_id]))

    context = {
        'event': event,
        'page': "event-details",
        'similar_by_place': similar_by_place,
        'similar_by_organization': similar_by_organization,
        'event_reviews': event_reviews,
        'today': today,
        'participations': event_p,
        'users_in_event': users_event
    }

    if (request.user.is_authenticated):
        context['event_user'] = event_user

    return render(request, 'front/event-details.html', context)



###########################################################################################################################################
# User Views
###########################################################################################################################################



@login_required
def edit_profile(request):
    """
    Edit the profile of the currently logged in :model:`auth.User`.

    **Parameters**

    ``request``
        The request object.

    **Context**

    ``orgs``
        A QuerySet of :model:`main.Organization` instances.

    **Post Parameters**

    ``form_type``
        The type of the form being submitted. This should be 'profile' for the profile form.

    ``first_name``
        The first name of the user.

    ``last_name``
        The last name of the user.

    ``username``
        The username of the user.

    ``date_birth``
        The birth date of the user.

    ``instagram_link``
        The Instagram link of the user.

    **Template:**

    :template:`front/edit-profile.html`
    """
    orgs = Organization.objects.all()
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            # Collect data from the profile form
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            date_birth = request.POST.get('date_birth')
            instagram_link = request.POST.get('instagram')
            email = request.POST.get('email')
            bio = request.POST.get('bio')

            # Update the user model
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.full_name = first_name + " " + last_name
            user.username = username
            user.email = email
            user.date_birth = date_birth
            user.instagram_link = instagram_link
            user.bio = bio

            # Save changes to both models
            user.save()

            # Display success message and redirect
            #messages.success(request, 'Your profile was successfully updated!')
            return redirect('my-profile')

        elif form_type == 'password':
            current_password = request.POST.get('curr_password')
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')

            if new_password == confirm_password:
                user = request.user
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Important to keep the user logged in
                    return redirect('my-profile')
                else:
                    message = "Pogrešna lozinka!"
                    return render(request, 'front/edit-profile.html', {"orgs": orgs, "message_pass": message})
            else:
                message = "Lozinke se ne podudaraju!"
                return render(request, 'front/edit-profile.html', {"orgs": orgs, "message_pass": message})
        elif form_type == 'become_org':

            existing_memberships = OrganizationUser.objects.filter(user=request.user, role__in=['member', 'admin'])
            if existing_memberships.exists():
                message = "Već ste član druge organizacije, ne možete postati organizator!"
                return render(request, 'front/edit-profile.html', {"orgs": orgs, "message": message})

            admins = User200.objects.filter(
                role='admin'
            )

            notification_type = NotificationType.objects.get(id=6)
            notifications = []
            for admin in admins:
                notification = Notification(
                    user=admin,
                    from_id=request.user.id,
                    from_type='user',
                    message=f"želi da postane organizator!",
                    notification_type=notification_type,
                    status='unread',
                    created_at=timezone.now()
                )
                notifications.append(notification)

            # Bulk create notifications
            Notification.objects.bulk_create(notifications)

            return redirect('my-profile')

    # Render the form with the current user's data
    return render(request, 'front/edit-profile.html', {"orgs": orgs, 'message': ""})

def forgot_password(request):
    """
    Edit the profile of the currently logged in :model:`auth.User`.

    **Parameters**

    ``request``
        The request object.

    **Context**

    ``orgs``
        A QuerySet of :model:`main.Organization` instances.

    **Post Parameters**

    ``form_type``
        The type of the form being submitted. This should be 'profile' for the profile form.

    ``first_name``
        The first name of the user.

    ``last_name``
        The last name of the user.

    ``username``
        The username of the user.

    ``date_birth``
        The birth date of the user.

    ``instagram_link``
        The Instagram link of the user.

    **Template:**

    :template:`front/edit-profile.html`
    """
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = User200.objects.make_random_password()
        send_mail(
            'Resetovanje lozinke',
            f'Postovani, vasa nova lozinka je: {new_password}',
            'vtomic03@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('index')
    return render(request, 'front/forgot-password.html')

def logout_user(request):
    """
    Log out the currently logged in user.

    **Parameters**
    
    ``request``
        The HTTP request object.

    **Template**

    :template:`front/logout.html`
    """
    logout(request)
    return redirect('index')

@login_required
def my_profile(request):
    """
    Display the profile of the currently logged in :model:`auth.User`.
    
    **Parameters**
    
    ``request``
        The request object.
        
    **Context**
    
    ``connections``
        A QuerySet of :model:`main.Connection` instances.
    
    ``orgs``
        A QuerySet of :model:`main.Organization` instances.
    
    **Template**
    
    :template:`front/my-profile.html`
    """
    connections = request.user.following.select_related('followee').filter(status='accepted')
    orgs = request.user.organizationuser_set.filter(role='member').all()
    return render(request, 'front/my-profile.html', { 'connections' : connections ,'page': "my-profile", 'orgs': orgs})

def profile_view(request, username):
    """
    Display the profile of a user.

    **Parameters**
        
            ``request``
                The request object.

            ``username``
                The username of the user whose profile is to be displayed.

    **Context**

            ``curr_user``
                An instance of :model:`main.User200`.

            ``page``
                A string representing the current page.

            ``conn_status``
                A string representing the connection status between the current user and the user whose profile is being viewed.

    **Template**

    :template:`front/profile.html`
    """
    try:
        user = User200.objects.get(username=username)
        if request.user.username == username:
            return redirect("my-profile")
    except User200.DoesNotExist:
        return custom_404_view(request, User200.DoesNotExist)
    conn_status = ''
    if request.user.is_authenticated:
        conn_status = Connection.objects.filter(follower=request.user, followee=user).first()
        if conn_status:
            conn_status = conn_status.status
        else:
            conn_status = ''
    connections = user.following.select_related('followee').filter(status='accepted')
    return render(request, 'front/profile.html',
           {'curr_user': user, 'page': "profile", 'conn_status': conn_status, 'conns': connections})

@remove_file_path_decorator
def register_user(request):
    """
    Register a new user.

    **Parameters**

    ``request``
        The HTTP request object.

    **Context**

    ``faculties``
        A QuerySet of :model:`main.Faculty` instances.

    **Post Parameters**

    ``fullname``
        The full name of the user.

    ``dob``
        The date of birth of the user.

    ``place``
        The city of the user.

    ``gender``
        The gender of the user.

    ``faculty``
        The ID of the faculty the user belongs to.

    ``username``
        The username of the user.

    ``email``
        The email of the user.

    **Template**

    :template:`front/sign-up-split.html`
    """
    faculties = Faculty.objects.all()
    if request.method == 'POST':
        # Retrieve fields from form
        full_name = request.POST.get('fullname')
        dob_str = request.POST.get('dob')
        city = request.POST.get('place')
        gender = request.POST.get('gender')
        faculty_id = request.POST.get('faculty')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        # Handle date
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        # Handle Faculty
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
        except Faculty.DoesNotExist:
            faculty = None  # or handle the error

        # Create new user
        if username and email and password:  # Basic validation
            parts = full_name.split(' ')
            if len(parts) > 1:
                ime = parts[0]
                prezime = parts[1]
            else:
                ime = parts[0]
                prezime = ''
            user = User200(
                full_name=full_name,
                first_name=ime,
                last_name=prezime,
                date_birth=dob,
                city=city,
                gender=gender if gender in ['M', 'F', 'O'] else None,
                faculty=faculty,
                username=username,
                email=email,
                password=make_password(password),
                role='regular'
            )
            file_path = request.session.pop('file_path', None)
            if file_path:
                with open(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)), 'rb') as f:
                    user.profile_picture = File(f, name=str(time.time()) + '.jpg')
                    user.save()
                os.remove(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)))
            else:
                user.profile_picture = File(open('static/images/avatar/placeholder.jpg', 'rb'),
                                            name=str(time.time()) + '.jpg')
                user.save()
            login(request, user)
            return redirect('index')  # Redirect after POST
        else:
            print("ERROR")

    # Display form if not POST or in case of errors
    return render(request, 'front/sign-up-split.html', {"faculties": faculties})

def user_login(request):
    """
    Log in a user.

    **Parameters**

    ``request``
        The HTTP request object.

    **Context**

    ``error_message``
        A string representing an error message.

    **Post Parameters**

    ``username``
        The username of the user.

    ``password``
        The password of the user.

    **Template**

    :template:`front/sign-in.html`
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            # Redirect to a success page or homepage
            return HttpResponseRedirect(reverse('index'))  # Adjust 'home' to your desired URL name
        else:
            # Return an invalid login message
            return render(request, 'front/sign-in.html', {'error_message': 'Invalid credentials. Please try again.'})

    return render(request, 'front/sign-in.html')

@login_required
@require_POST
def update_mutual_connections(request):
    """
    Update mutual connections.

    **Parameters**

    ``request``
        The HTTP request object.    

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    if request.method == 'POST':
        user = request.user
        connections = request.user.following.select_related('followee').filter(status='accepted')
        data = {}
        for conn in connections:
            data[conn.followee.id] = mutual_conns(conn.followee, user)
        return JsonResponse(data)



###########################################################################################################################################
# Organization Views
###########################################################################################################################################



def organizations(request):
    """
    Display a list of organizations.

    **Parameters**
    
        ``request``
            The HTTP request object.
    
    **Context**

        ``groups``
            A QuerySet of :model:`main.Organization` instances.
        
        ``page``
            A string representing the current page.

    **Template**

    :template:`front/groups.html`
    """
    can_create = False
    if request.user.is_authenticated:
        can_create = request.user.role == 'organizer' and not request.user.organizationuser_set.filter(role ='member').exists()

    # Retrieve all events from the database
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'filter1' or form_type == 'filter2':
            name = request.POST.get('name')
            order = request.POST.get('order')
            if name:
                orgs = Organization.objects.filter(name__icontains=name)
            else:
                name = "Pretraga..."
                orgs = Organization.objects.all()
            if order == "newest":
                orgs = orgs.order_by('-created_at')
            elif order == "rating":
                orgs = orgs.order_by('-total_rating')
            else:
                orgs = orgs.order_by('name')

            for org in orgs:
                org.members_list = org.organizationuser_set.filter(role='member')
                org.followers = org.organizationuser_set.filter(role='follower').count()

            return render(request, 'front/groups.html',
                          {'groups': orgs, 'page': "organizations", 'name': name, 'order': order, 'can_create': can_create})
        # Retrieve fields from form
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Create new organization
        if name and description:
            org = Organization(
                name=name,
                description=description,
                total_rating=0,
                count_rating=0,
                created_at=datetime.now()
            )
            file_path = request.session.pop('file_path', None)
            if file_path:
                with open(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)), 'rb') as f:
                    org.picture = File(f, name=str(time.time()) + '.jpg')
                    org.save()
                os.remove(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)))
            else:
                org.picture = File(open('static/images/avatar/placeholder.jpg', 'rb'), name=str(time.time()) + '.jpg')
                org.save()

            org_user = OrganizationUser(user=request.user, org=org, role='member', join_date=datetime.now())
            org_user.save()

            stud_org = StudentOrg(org=org, faculty=request.user.faculty)
            stud_org.save()

            return redirect('organizations')
    orgs = Organization.objects.all()
    name = "Pretraga..."
    order = "alphabetical"

    for org in orgs:
        org.members_list = org.organizationuser_set.filter(role='member')
        org.followers = org.organizationuser_set.filter(role='follower').count()
    # Render a template with the list of events
    return render(request, 'front/groups.html', {'groups': orgs, 'page': "organizations", 'name': name, 'order': order, 'can_create': can_create})

def organization_details(request, org_id):
    """
    Display the details of an individual :model:`main.Organization`.

    **Parameters**
    
        ``request``
            The request object.
    
        ``org_id``
            The ID of the :model:`main.Organization` whose details are to be displayed.

    **Context**

        ``org``
            An instance of :model:`main.Organization`.

        ``page``
            A string representing the current page.

        ``members``
            A QuerySet of :model:`main.OrganizationUser` instances.

        ``can_join``
            A boolean indicating whether the current user can join the organization.

        ``is_following``
            A boolean indicating whether the current user is following the organization.

    **Template**

    :template:`front/group-details.html`
    """
    try:
        # Get the organization with the specified ID
        organization = Organization.objects.get(org_id=org_id)
    except Organization.DoesNotExist:
        # Handle the case where the organization does not exist
        return render(request, '404.html', status=404)

    can_join = False
    if request.user.is_authenticated:
        can_join = not OrganizationUser.objects.filter(user=request.user, role='member').exists()

    is_following = False
    if request.user.is_authenticated:
        is_following = organization.organizationuser_set.filter(user=request.user, role='follower').exists()

    members = organization.organizationuser_set.filter(role='member')
    if request.user.is_authenticated:
        for member in members:
            if member.user == request.user:
                member.is_current_user = True
            conn_status = Connection.objects.filter(follower=request.user, followee=member.user).first()
            if conn_status:
                conn_status = conn_status.status
            else:
                conn_status = ''
            member.conn_status = conn_status


    # Render the event detail template with the organization data
    return render(request, 'front/group-details.html',
                  {'org': organization, 'page': "organization-details", 'members': members, 'can_join': can_join,
                   'is_following': is_following})



###########################################################################################################################################
# Place Views
###########################################################################################################################################



def locations(request):
    """
    Display a list of locations.

    **Parameters**
    
    ``request``
        The HTTP request object.
    
    **Context**
        
        ``locations``
            A QuerySet of :model:`main.Place` instances.
        
        ``page``
            A string representing the current page.
    
    **Template**

    :template:`front/locations.html`
    """
    # Retrieve all events from the database
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'filter1' or form_type == 'filter2':
            name = request.POST.get('name')
            order = request.POST.get('order')
            placeType = request.POST.get('placeType')
            if name:
                locations = Place.objects.filter(name__icontains=name)
            else:
                name = "Pretraga..."
                locations = Place.objects.all()

            if order == "rating":
                locations = locations.order_by('-total_rating')
            else:
                locations = locations.order_by('name')

            if placeType != "category":
                locations = locations.filter(place_type__name=placeType)

            placeTypes = PlaceType.objects.all()
            return render(request, 'front/locations.html',
                          {'locations': locations, 'page': "locations", 'name': name, 'order': order, 'placeTypes': placeTypes, 'placeType': placeType})
        # Retrieve fields from form
        name = request.POST.get('name')
        description = request.POST.get('description')
        working_hours = request.POST.get('working_hours')
        address = request.POST.get('address')
        type = request.POST.get('type')
        google_maps = request.POST.get('google_maps')
        placetype = PlaceType.objects.get(name=type)
        # Create new location
        if name and description:
            location = Place(
                name=name,
                description=description,
                working_hours=working_hours,
                address=address,
                place_type=placetype,
                google_maps_url=google_maps,
                total_rating=0,
                count_rating=0
            )
            file_path = request.session.pop('file_path', None)
            if file_path:
                with open(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)), 'rb') as f:
                    location.picture = File(f, name=str(time.time()) + '.jpg')
                    location.save()
                os.remove(os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(file_path)))
            else:
                location.picture = File(open('static/images/avatar/placeholder.jpg', 'rb'),
                                        name=str(time.time()) + '.jpg')
                location.save()

            return redirect('locations')
    locations = Place.objects.all()
    for location in locations:
        if location.count_rating > 0:
            location.average_rating = str(location.total_rating / location.count_rating)
        else:
            location.average_rating = "0.0"

    name = "Pretraga..."
    order = "alphabetical"
    placeTypes = PlaceType.objects.all()
    placeType = "category"
    # Render a template with the list of events
    return render(request, 'front/locations.html',
                  {'locations': locations, 'page': "locations", 'name': name, 'order': order, 'placeTypes': placeTypes, 'placeType': placeType})

def location_details(request, place_id):
    """
    Display the details of an individual :model:`main.Place`.

    **Parameters**
    
    ``request``
        The request object.

    ``place_id``
        The ID of the :model:`main.Place` whose details are to be displayed.
    
    **Context**
        
    ``place``
        An instance of :model:`main.Place`.

    ``page``
        A string representing the current page.
    
    **Template**
        
    :template:`front/location-details.html`
    """
    try:
        # Get the event with the specified ID
        location = Place.objects.get(place_id=place_id)
    except Event.DoesNotExist:
        # Handle the case where the event does not exist
        return render(request, '404.html', status=404)

    # Render the event detail template with the event data
    return render(request, 'front/location-details.html', {'place': location, 'page': "location-details"})



###########################################################################################################################################
# Notification Views
###########################################################################################################################################



def accept_conn_request(request):
    """
    Accept a connection request.

    **Parameters**
    
        ``request``
            The HTTP request object.

    **Post Parameters**

        ``notification_id``
            The ID of the notification to accept.

    **Returns**
    
        ``JsonResponse``
            A JSON response indicating the status of the operation.
    """

    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')

    try:
        notif = Notification.objects.get(notification_id=notification_id)

        follower = User200.objects.get(id=notif.from_id)

        connection_request = Connection.objects.get(follower=follower, followee=request.user, status='pending')

        connection_request.status = 'accepted'
        connection_request.follow_date = timezone.now()
        connection_request.save()


        Connection.objects.create(
            follower=request.user,
            followee=follower,
            follow_date=timezone.now(),
            status='accepted'
        ).save()

        # Send acceptance notification to the follower
        notification_type = NotificationType.objects.get(name='standard')
        acceptance_message = f"je prihvatio vaš zahtev za konekciju."
        Notification.objects.create(
            user=follower,
            from_id=request.user.id,
            from_type='user',
            message=acceptance_message,
            notification_type=notification_type,
            status='unread',
            created_at=timezone.now()
        ).save()

        notif.delete()

        return JsonResponse({'status': 'success'})

    except User200.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'})

def accept_join_request(request):
    """
    Accepts a join request from a user to join an organization.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the operation.

    Raises:
        Organization.DoesNotExist: If the organization specified in the join request does not exist.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    try:
        notif = Notification.objects.get(notification_id=notification_id)
        org = Organization.objects.filter(name=re.search(r"želi da se učlani u (.+)", notif.message).group(1)).first()

        # Create OrganizationUser entry
        OrganizationUser.objects.create(
            org=org,
            user=User200.objects.get(id=notif.from_id),
            role='member',  # or whatever role is appropriate
            join_date=timezone.now()
        )

        # Delete other notifications with the same message and notification type
        Notification.objects.filter(
            from_id=notif.from_id,
            message=notif.message
        ).delete()

        notification_type = NotificationType.objects.get(id=4)
        notification = Notification(
            user=User200.objects.filter(id=notif.from_id).first(),
            from_id=request.user.id,
            from_type='user',
            message=f"vas je prihvatio/la u {org}",
            notification_type=notification_type,
            status='unread',
            created_at=timezone.now()
        )
        notification.save()

        return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def accept_org_request(request):
    """
    Accepts an organization request and updates the user's role to 'organizer'.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the operation.

    Raises:
        Organization.DoesNotExist: If the organization does not exist.
    """

    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    try:
        notif = Notification.objects.get(notification_id=notification_id)

        fresh_organizer = User200.objects.filter(id=notif.from_id).first()

        fresh_organizer.role = 'organizer'
        fresh_organizer.save()

        # Delete other notifications with the same message and notification type
        Notification.objects.filter(
            from_id=notif.from_id,
            message=notif.message
        ).delete()

        notification_type = NotificationType.objects.get(id=4)
        notification = Notification(
            user=fresh_organizer,
            from_id=request.user.id,
            from_type='user',
            message=f"je odobrio tvoj zahtev. Sada si organizator!",
            notification_type=notification_type,
            status='unread',
            created_at=timezone.now()
        )
        notification.save()

        return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def accept_event_invite(request):
    """
    Accepts an event invitation.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        JsonResponse: A JSON response indicating the status of the operation.
        
    Raises:
        Event.DoesNotExist: If the event does not exist.
    """
    data = json.loads(request.body.decode('utf-8'))
    event_name = Notification.objects.filter(notification_id=data.get('notification_id')).values_list('message', flat=True).first()
    try:
        event = Event.objects.get(name=event_name)
        user = request.user
        # Get or create the EventUser instance
        event_user, created = EventUser.objects.get_or_create(user=user, event=event)

        if created:
            event_user.status = 'interested'
            event_user.created_at = timezone.now()
            event_user.save()

            notif = Notification.objects.get(notification_id=data.get('notification_id'))
            notif.delete()

            return JsonResponse({'status': 'success'})
        else:
            event_user.delete()
            return JsonResponse({'status': 'canceled'})
    except Event.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event does not exist'})

def decline_join_request(request):
    """
    Declines a join request from a user to join an organization.

    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        JsonResponse: A JSON response indicating the status of the operation.

    Raises:
        Organization.DoesNotExist: If the organization specified in the join request does not exist.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    try:
        notif = Notification.objects.get(notification_id=notification_id)

        # Delete other notifications with the same message and notification type
        Notification.objects.filter(
            from_id=notif.from_id,
            message=notif.message
        ).delete()


        return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def decline_event_invite(request):
    """
    Declines an event invitation.

    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        JsonResponse: A JSON response indicating the status of the operation.
    
    Raises:
        Event.DoesNotExist: If the event does not exist.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    try:
        notif = Notification.objects.get(notification_id=notification_id)

        notif.delete()

        return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

@login_required
def delete_all_notifications(request):
    """
    Delete all notifications.

    **Parameters**

    ``request``
        The HTTP request object.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    notifications = Notification.objects.filter(user=request.user)
    notifications.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_one_notification(request):
    """
    Delete one notification.

    **Parameters**

    ``request``
        The HTTP request object.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    notification = Notification.objects.filter(user=request.user, notification_id=notification_id)
    notification.delete()
    return JsonResponse({'status': 'success'})

def decline_conn_request(request):
    """
    Decline a connection request.
    
    **Parameters**
    
    ``request``
        The HTTP request object.
        
    **Post Parameters**

    ``notification_id``
        The ID of the notification to decline.
        
    **Returns**
    
    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    try:
        notif = Notification.objects.get(notification_id=notification_id)

        follower = User200.objects.get(id=notif.from_id)

        # Retrieve the pending connection request
        connection_request = Connection.objects.get(follower=follower, followee=request.user, status='pending')

        connection_request.status = 'declined'
        connection_request.save()

        # Send decline notification to the follower
        notification_type = NotificationType.objects.get(name='standard')
        decline_message = f"je odbio vaš zahtev za konekciju."
        Notification.objects.create(
            user=follower,
            from_id=request.user.id,
            from_type='user',
            message=decline_message,
            notification_type=notification_type,
            status='unread',
            created_at=timezone.now()
        ).save()


        # Delete other notifications with the same message and notification type
        notif.delete()

        return JsonResponse({'status': 'success'})

    except User200.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist'})
 
@login_required
@require_POST
def follow_organization(request):
    """
    Follow an organization.

    **Parameters**

    ``request``
        The HTTP request object.

    **Post Parameters**

    ``org_id``
        The ID of the organization to follow.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.

    **Raises**

    ``Organization.DoesNotExist``
        If the organization specified in the request does not exist.
    """
    data = json.loads(request.body.decode('utf-8'))
    org_id = data.get('org_id')
    try:
        org = Organization.objects.get(org_id=org_id)
        user = request.user
        # Get or create the OrganizationUser instance
        org_user, created = OrganizationUser.objects.get_or_create(user=user, org=org)

        if created:
            org_user.role = 'follower'
            org_user.join_date = timezone.now()
            org_user.save()
            return JsonResponse({'status': 'success'})
        else:
            org_user.delete()
            return JsonResponse({'status': 'canceled'})
    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def invite_followers_to_party(request):
    """
    Invite followers to a party.
    
    **Parameters**
    
    ``request``
        The HTTP request object.
    
    **Post Parameters**
    
    ``event_id``
        The ID of the event to invite followers to.
        
    **Template**

    :template:`front/invite-followers-to-party.html`
    """
    data = json.loads(request.body.decode('utf-8'))
    event_id = data.get('event_id')
    try:
        event = Event.objects.get(event_id=event_id)
        user = request.user
        org = Organization.objects.filter(organizationuser__user=user, organizationuser__role='member').first()
        followers = OrganizationUser.objects.filter(org=org, role='follower').values_list('user', flat=True)
        follower_users = User200.objects.filter(id__in=followers)

        notification_type = NotificationType.objects.get(id=2)
        notifications = []
        for follower in follower_users:
            if event not in follower.event_participations.all():
                notification = Notification(
                    user=follower,
                    from_id=user.id,
                    from_type='user',
                    message=event,
                    notification_type=notification_type,
                    status='unread',
                    created_at=timezone.now()
                )
                notifications.append(notification)

        # Bulk create notifications
        Notification.objects.bulk_create(notifications)
        return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def join_organization(request):
    """
    Join an organization.
    
    **Parameters**
    
    ``request``
        The HTTP request object.
    
    **Post Parameters**
    
    ``org_id``
        The ID of the organization to join.
    
    **Template**
    
    :template:`front/join-organization.html`
    """
    data = json.loads(request.body.decode('utf-8'))
    org_id = data.get('org_id')
    try:
        org = Organization.objects.get(org_id=org_id)
        user = request.user

        message = f"želi da se učlani u {org}"
        notification_exists = Notification.objects.filter(message=message, from_id=user.id).exists()
        if notification_exists:
            Notification.objects.filter(message=message, from_id=user.id).delete()
            return JsonResponse({'status': 'canceled'})
        else:
            organizers = User200.objects.filter(
                organizationuser__org=org,
                role='organizer'
            )

            notification_type = NotificationType.objects.get(id=5)
            notifications = []
            for organizer in organizers:
                notification = Notification(
                    user=organizer,
                    from_id=user.id,
                    from_type='user',
                    message=f"želi da se učlani u {org}",
                    notification_type=notification_type,
                    status='unread',
                    created_at=timezone.now()
                )
                notifications.append(notification)

            # Bulk create notifications
            Notification.objects.bulk_create(notifications)
            return JsonResponse({'status': 'success'})

    except Organization.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization does not exist'})

def leave_organization(request):
    """
    Leave an organization.

    **Parameters**

    ``request``
        The HTTP request object.
    
    **Post Parameters**

    ``org_id``
        The ID of the organization to leave.

    **Template**

    :template:`front/leave-organization.html`
    """
    data = json.loads(request.body.decode('utf-8'))
    org_id = data.get('org_id')
    try:
        org = Organization.objects.get(org_id=org_id)
        user = User200.objects.get(id=request.user.id)

        OrganizationUser.objects.filter(org=org, user=user).delete()
        return JsonResponse({'status': 'success'})
    except KeyError:
        return JsonResponse({'status': 'error'})

@login_required
@require_POST
def mark_interested(request):
    """
    Mark an event as interested.

    **Parameters**

    ``request``
        The HTTP request object.
    
    **Post Parameters**

    ``event_id``
        The ID of the event to mark as interested.
    
    **Template**

    :template:`front/mark-interested.html`
    """
    data = json.loads(request.body.decode('utf-8'))
    event_id = data.get('event_id')
    try:
        event = Event.objects.get(event_id=event_id)
        user = request.user
        # Get or create the EventUser instance
        event_user, created = EventUser.objects.get_or_create(user=user, event=event)

        if created:
            event_user.status = 'interested'
            event_user.created_at = timezone.now()
            event_user.save()
            return JsonResponse({'status': 'success'})
        else:
            event_user.delete()
            return JsonResponse({'status': 'canceled'})
    except Event.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Event does not exist'})

@login_required
def mark_all_notifications_read(request):
    """
    Mark all notifications as read.

    **Parameters**

    ``request``
        The HTTP request object.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    notifications = Notification.objects.filter(user=request.user, status='unread')
    notifications.update(status='read')
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_read(request):
    """
    Mark all notifications as read.
    
    **Parameters**
    
    ``request``
        The HTTP request object.
        
    **Returns**
    
    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """

    notifications = Notification.objects.filter(user=request.user, status='unread')
    notifications.update(status='read')
    return JsonResponse({'status': 'success'})

@login_required
def mark_one_read(request):
    """
    Mark one notification as read.

    **Parameters**

    ``request``
        The HTTP request object.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    data = json.loads(request.body.decode('utf-8'))
    notification_id = data.get('notification_id')
    notification = Notification.objects.filter(user=request.user, notification_id=notification_id)
    notification.update(status='read')
    return JsonResponse({'status': 'success'})

def notifications(request):
    """
    Display the notifications of the currently logged in :model:`auth.User`.

    **Parameters**

    ``request``
        The request object.
    
    **Context**

    ``notifications``
        A QuerySet of :model:`main.Notification` instances.
    
    **Template**

    :template:`front/notifications.html`
    """
    nots = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'front/notifications.html', {'notifications': nots, 'page': "notifications"})

@login_required
@require_POST
def remove_followee(request):
    """
    Remove a followee.

    **Parameters**

    ``request``
        The HTTP request object.

    **Post Parameters**

    ``followee_id``
        The ID of the followee to remove.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    data = json.loads(request.body.decode('utf-8'))
    followee_id = data.get('followee_id')
    try:
        conn = Connection.objects.get(followee_id=followee_id, follower_id=request.user.id)
        conn2 = Connection.objects.get(followee_id=request.user.id, follower_id=followee_id)
        conn2.delete()
        conn.delete()
        return JsonResponse({'status': 'success'})
    except Connection.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Doslo je do greske, molimo vas pokusajte kasnije.'})

@login_required
@require_POST
def send_connection_request(request):
    """
    Send a connection request.

    **Parameters**

    ``request``
        The HTTP request object.

    **Post Parameters**

    ``followee_id``
        The ID of the user to send the connection request to.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    data = json.loads(request.body.decode('utf-8'))
    recipient_id = data.get('followeeId')

    try:
        recipient = User200.objects.get(id=recipient_id)

        # Check if a connection request already exists
        existing_request = Connection.objects.filter(follower=request.user, followee=recipient,
                                                     status='pending').first()
        if existing_request:
            notification = Notification.objects.filter(from_id=request.user.id, user=recipient, notification_type__name='connection_request')
            if notification:
                notification.delete()
            existing_request.delete()
            return JsonResponse({'status': 'canceled'})

        # Create a new connection request
        Connection.objects.create(
            follower=request.user,
            followee=recipient,
            follow_date=timezone.now(),
            status='pending'
        )

        # Send a notification to the recipient
        notification_type = NotificationType.objects.get(name='connection_request')
        notification = Notification(
            user=recipient,
            from_id=request.user.id,
            from_type='user',
            message=f"{request.user.username} wants to connect with you.",
            notification_type=notification_type,
            status='unread',
            created_at=timezone.now()
        )
        notification.save()

        return JsonResponse({'status': 'success'})

    except User200.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Recipient user does not exist'})



###########################################################################################################################################
# Other Views
###########################################################################################################################################



def custom_404_view(request, exception):
    """
    Display a custom 404 error page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that was raised.
    
    Returns:
        HttpResponse: A response containing the custom 404 error page.
    """
    return render(request, 'front/error-404.html', status=404)

def index(request):
    """
    Display the home page.
    
    ***Parameters***
    
    ``request``
        The request object.
        
    ***Context***
    
    ``events``
        A QuerySet of :model:`main.Event` instances.
    
    ``places``
        A QuerySet of :model:`main.Place` instances.
        
    ``groups``
        A QuerySet of :model:`main.Organization` instances.
        
    ``page``
        A string representing the current page.
        
    ``participations``
        A QuerySet of :model:`main.EventParticipation` instances related to the current user.
        
    ***Template***
    
    :template:`front/index.html`
    """
    now = timezone.now().date()
    top_events = (
        Event.objects.filter(date__gt=now)
        .annotate(
            users_interested=Count('eventuser', filter=Q(eventuser__status='interested')),
            users_going=Count('eventuser', filter=Q(eventuser__status='going'))
        )
        .annotate(
            rank=ExpressionWrapper(
                F('users_interested') + F('users_going') * 2,
                output_field=IntegerField()
            )
        )
        .order_by('-rank')[:4]
    )

    top_four_places = Place.objects.annotate(
        rating_product=ExpressionWrapper(
            F('total_rating') * F('count_rating'),
            output_field=IntegerField()
        )
    ).order_by('-rating_product')[:4]

    top_four_orgs = Organization.objects.annotate(
        rating_product=ExpressionWrapper(
            F('total_rating') * F('count_rating'),
            output_field=IntegerField()
        )
    ).order_by('-rating_product')[:3]

    for org in top_four_orgs:
        org.members_list = org.organizationuser_set.filter(role='member')
        org.followers = org.organizationuser_set.filter(role='follower').count()
        org.users_list = org.organizationuser_set.all()

    try:
        event_p = request.user.event_participations.all()
    except:
        event_p = None

    return render(request, 'front/index.html', {'events': top_events, 'places': top_four_places, 'groups': top_four_orgs, 'page': "index", 'participations': event_p})

@csrf_exempt
def upload(request):
    """
    Upload a file.

    **Parameters**

    ``request``
        The HTTP request object.

    **Returns**

    ``JsonResponse``
        A JSON response indicating the status of the operation.
    """
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
            filename = fs.save(str(time.time()), file)
            file_url = fs.url(filename)
            request.session['file_path'] = file_url
            return JsonResponse({'message': 'File uploaded successfully'})
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
