#Created by: 
#   Vanja Tomic 0289/21
#   Vladimir Bogojevic 0387/21

# custom_filters.py
from datetime import timedelta

from django import template
from studiranje200.models import *
from django.utils import timezone
import re

register = template.Library()

@register.filter
def users_going_to_event(event, status='going'):
    """
    Custom filter to get users going to the specified event.
    """
    return EventUser.objects.filter(event=event, status=status).values_list('user', flat=True).count()

@register.filter
def users_interested_in_event(event, status='interested'):
    """
    Custom filter to get users interested to the specified event.
    """
    return EventUser.objects.filter(event=event, status=status).values_list('user', flat=True).count()

@register.filter
def date_joined(org, user):
    """
    Custom filter to get join_date for user and organizations.
    """
    return OrganizationUser.objects.filter(org=org, user=user).values_list('join_date', flat=True).first()

@register.filter
def role_in_org(org, user):
    """
    Custom filter to get role for user and organizations.
    """
    return OrganizationUser.objects.filter(org=org, user=user).values_list('role', flat=True).first()

@register.filter
def sledeci_event(events):
    print(events)
    """
    Custom filter to get next event for user.
    """
    now = timezone.now().date()
    next_event = events.filter(date__gt=now).order_by('date').first()
    if next_event is None:
        return "Nema događaja"
    return f"{next_event.name}  {next_event.date} {next_event.time.strftime('%H:%M')}"

@register.filter
def sledeci_event_id(events):
    print(events)
    """
    Custom filter to get next event for user.
    """
    now = timezone.now().date()
    next_event = events.filter(date__gt=now).order_by('date').first()
    return next_event.event_id

@register.filter
def prethodna_tri_eventa(events):
    print(events)
    """
    Custom filter to get three next events for user (skips first).
    """
    now = timezone.now().date()
    next_events = events.filter(date__lt=now).order_by('date')[0:3]
    return next_events

@register.filter
def mutual_conns(user1, user2):
    """
    Custom filter to get mutual connections between two users.
    """
    user1_following = Connection.objects.filter(follower=user1).values_list('followee', flat=True)
    user2_following = Connection.objects.filter(follower=user2).values_list('followee', flat=True)

    mutual_followees = set(user1_following).intersection(set(user2_following))

    return len(mutual_followees)

@register.filter
def rating(place):
    """
    Custom filter to get rating for place.
    """
    count = Place.objects.filter(name=place).values_list('count_rating', flat=True).first()
    total = Place.objects.filter(name=place).values_list('total_rating', flat=True).first()
    if total == 0:
        return "0.0"
    else:
        return "{:.1f}".format(float(total) / count)


@register.filter
def rating_org(org):
    """
    Custom filter to get rating for organization.
    """
    count = Organization.objects.filter(name=org).values_list('count_rating', flat=True).first()
    total = Organization.objects.filter(name=org).values_list('total_rating', flat=True).first()
    if total == 0:
        return "0.0"
    else:
        return "{:.1f}".format(float(total) / count)

@register.filter(name='truncate_after_second_comma')
def truncate_after_second_comma(value):
    """
    Truncate a string after the second comma.
    """
    if not isinstance(value, str):
        return value

    parts = value.split(',', 2)
    if len(parts) > 2:
        truncated_value = ','.join(parts[:2])
    else:
        truncated_value = value

    # If the truncated value is longer than 30 characters, cut it and add '...'
    if len(truncated_value) > 30:
        return truncated_value[:30] + '...'

    return truncated_value

@register.filter
def count_going_events(user):
    """
    Custom filter to get count of events user is going to.
    """
    if isinstance(user, User200):
        return EventUser.objects.filter(user=user, status='going').count()
    return 0

@register.filter
def count_accepted_connections(user):
    """
    Custom filter to get count of accepted connections for user.
    """
    if isinstance(user, User200):
        return Connection.objects.filter(
            models.Q(follower=user, status='accepted')
        ).count()
    return 0


@register.filter
def get_sender_user(from_id):
    """
    Custom filter to get sender user.
    """
    try:
        return User200.objects.get(pk=from_id)
    except User200.DoesNotExist:
        return None

@register.filter
def get_sender_organization(from_id):
    """
    Custom filter to get sender organization.
    """
    try:
        return Organization.objects.get(org_id=from_id)
    except Organization.DoesNotExist:
        return None


@register.filter
def sent_request(user, org):
    """
    Custom filter to check if user has sent request to join organization.
    """
    message = f"želi da se učlani u {org}"

    return Notification.objects.filter(message=message, from_id=user.id).exists()


@register.filter
def non_followers(org):
    """
    Custom filter to get non-followers for organization.
    """
    return User200.objects.filter(organizationuser__org=org).exclude(organizationuser__role='follower')


@register.filter
def event_id(event_name):
    """
    Custom filter to get event id by name.
    """
    return Event.objects.filter(name=event_name).values_list('event_id', flat=True).first()


@register.filter
def pendig_org_request(user):
    """
    Custom filter to check if user has pending organization request.
    """

    notif = NotificationType.objects.filter(id=6).first()

    return Notification.objects.filter(notification_type=notif, from_id=user.id).exists()

@register.filter
def cant_invite(event):
    """
    Custom filter to check if user can invite to event.
    """
    notification_type = NotificationType.objects.get(id=2)
    one_day_ago = timezone.now() - timedelta(days=1)
    return Notification.objects.filter(
        message=event,
        notification_type_id=notification_type,
        created_at__gte=one_day_ago
    ).exists()


@register.filter
def get_organization(user):
    """
    Custom filter to get organization for user.
    """
    return Organization.objects.filter(
        organizationuser__user=user,
        organizationuser__role='member'
    ).all()

@register.filter
def event_object(name):
    """
    Custom filter to get event object by name.
    """
    return Event.objects.filter(
        name=name
    ).first()

@register.filter
def extract_segment(url):
    """
    Custom filter to extract segment from URL.
    """
    parts = url.rstrip('/').split('/')
    if len(parts) > 1:
        return parts[-1]  # Get the second-to-last segment
    return url