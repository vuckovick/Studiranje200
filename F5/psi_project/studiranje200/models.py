#Created by: 
#   Vanja Tomic 0289/21
#   Konstantin Vuckovic 0524/21
#   Vladimir Bogojevic 0387/21
#   Mihajlo Antonijevic 0382/21

from django.contrib.auth.models import AbstractUser
from django.db import models


# Dynamic Enum Models
class PlaceType(models.Model):
    """
    Stores a single place type entry, related to :model:`main.Place`.
    """
    name = models.CharField(max_length=50, unique=True, help_text='Name of the place type')
    picture = models.CharField(max_length=255, null=True, blank=True, help_text='Picture of the place type')

    def __str__(self):
        return self.name

class NotificationType(models.Model):
    """
    Stores a single notification type entry, related to :model:`main.Notification`.
    """
    name = models.CharField(max_length=50, unique=True, help_text='Name of the notification type')

    def __str__(self):
        return self.name


class EventType(models.Model):
    """
    Stores a single event type entry, related to :model:`main.Event`.
    """
    name = models.CharField(max_length=50, unique=True, help_text='Name of the event type')

    def __str__(self):
        return self.name


# Main Models
class User200(AbstractUser):
    """
    Stores a single user entry, related to :model:`main.Connection`, :model:`main.EventUser`, :model:`main.Notification`, :model:`main.OrganizationUser`, :model:`main.EventReview`.

    Methods:
        get_notifications(): Returns the unread notifications for the user.
    """
    # Additional fields
    full_name = models.CharField(max_length=255, null=True, blank=True, help_text='Full name of the user')
    date_birth = models.DateField(null=True, blank=True, help_text='Date of birth of the user')
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], help_text="The gender of the user. Choices are 'M' for Male and 'F' for Female.")
    city = models.CharField(max_length=255, null=True, blank=True, help_text='City where the user resides')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, null=True, blank=True, help_text='The faculty the user is associated with')
    instagram_link = models.CharField(max_length=255, null=True, blank=True, help_text='Instagram profile link of the user')
    profile_picture = models.ImageField(upload_to='profile_pictures/', help_text='Profile picture of the user')
    bio = models.TextField(null=True, blank=True, help_text='Biography of the user')
    role = models.CharField(max_length=255, choices=[('regular', 'Regular'), ('organizer', 'Organizer'), ('admin', 'Admin')], help_text='The role of the user. Choices are "regular", "organizer", and "admin".')
    unread_notifications = models.IntegerField(null=True, blank=True, help_text='Number of unread notifications for the user')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the user was created')
    connections = models.ManyToManyField('self', through='Connection', symmetrical=False, related_name='connected_to', help_text='Connections of the user with other users')
    event_participations = models.ManyToManyField('Event', through='EventUser', related_name='user_participants', help_text='Events in which the user is participating')
    reviews = models.ManyToManyField('Event', through='EventReview', related_name='user_reviewers', help_text='Events for which the user has provided reviews')
    organizations = models.ManyToManyField('Organization', through='OrganizationUser', related_name='user_members', help_text='Organizations the user is a member of')

    def get_notifications(self):
        """
        Returns the unread notifications for the user.

        Returns:
            QuerySet: A queryset of unread notifications for the user, ordered by creation timestamp in descending order.
        """
        return self.notifications.filter(status='unread').order_by('-created_at')

    def __str__(self):
        return self.username


class Faculty(models.Model):
    """
    Stores a single faculty entry, related to :model:`main.StudentOrg`.
    """
    faculty_id = models.AutoField(primary_key=True, help_text='The unique identifier of the faculty')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Name of the faculty')
    city = models.CharField(max_length=255, null=True, blank=True, help_text='City where the faculty is located')
    tag = models.CharField(max_length=255, null=True, blank=True, help_text='Short name of the faculty')

    def __str__(self):
        return self.name


class Place(models.Model):
    """
    Stores a single place entry, related to :model:`main.Event`.
    """
    place_id = models.AutoField(primary_key=True, help_text='The unique identifier of the place')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Name of the place')
    description = models.CharField(max_length=255, null=True, blank=True, help_text='Description of the place')
    working_hours = models.CharField(max_length=255, null=True, blank=True, help_text='Working hours of the place')
    address = models.CharField(max_length=255, null=True, blank=True, help_text='Address of the place')
    place_type = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, null=True, blank=True, help_text='Type of the place')
    picture = models.ImageField(upload_to='places_pictures/', help_text='Picture of the place')
    total_rating = models.IntegerField(null=True, blank=True, help_text='Total rating of the place')
    count_rating = models.IntegerField(null=True, blank=True, help_text='Number of ratings of the place')
    google_maps_url = models.CharField(max_length=255, null=True, blank=True, help_text='Google Maps URL of the place')
    website_url = models.CharField(max_length=255, null=True, blank=True, help_text='Website URL of the place')

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    Stores a single organization entry, related to :model:`main.OrganizationUser`, :model:`main.Notification`.
    """
    org_id = models.AutoField(primary_key=True, help_text='The unique identifier of the organization')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Name of the organization')
    description = models.TextField(null=True, blank=True, help_text='Description of the organization')
    picture = models.ImageField(upload_to='organization_pictures/', help_text='Picture of the organization')
    total_rating = models.IntegerField(null=True, blank=True, help_text='Total rating of the organization')
    count_rating = models.IntegerField(null=True, blank=True, help_text='Number of ratings of the organization')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the organization was created')
    members = models.ManyToManyField(User200, through='OrganizationUser', related_name='organization_members', help_text='Members of the organization')

    def __str__(self):
        return self.name


class Connection(models.Model):
    """
    Stores a single connection entry, related to :model:`main.User200`.
    """
    follower = models.ForeignKey(User200, on_delete=models.CASCADE, related_name='following', null=True, blank=True, help_text='The user who is following another user')
    followee = models.ForeignKey(User200, on_delete=models.CASCADE, related_name='followers', null=True, blank=True, help_text='The user who is being followed by another user')
    follow_date = models.DateTimeField(null=True, blank=True, help_text='Timestamp when the connection was established')
    status = models.CharField(max_length=255, choices=[('accepted', 'Accepted'), ('declined', 'Declined'), ('pending', 'Pending')], help_text='The status of the connection request. Choices are "accepted", "declined", and "pending"')

    class Meta:
        unique_together = ('follower', 'followee')


class Event(models.Model):
    """
    Stores a single event entry, related to :model:`main.EventReview`, :model:`main.EventUser`, :model:`main.Place`, :model:`main.Organization`, :model:`main.EventType`, :model:`main.User200`.
    """
    event_id = models.AutoField(primary_key=True, help_text='The unique identifier of the event')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Name of the event')
    description = models.TextField(null=True, blank=True, help_text='Description of the event')
    date = models.DateField(null=True, blank=True, help_text='Date of the event')
    time = models.TimeField(null=True, blank=True, help_text='Time of the event')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name='events', null=True, blank=True, help_text='The organization hosting the event')
    status = models.CharField(max_length=255, choices=[('draft', 'Draft'), ('published', 'Published'), ('cancelled', 'Cancelled')], help_text='The status of the event. Choices are "draft", "published", and "cancelled"')
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True, help_text='Type of the event')
    picture = models.ImageField(upload_to='event_pictures/', help_text='Picture of the event')
    total_rating = models.IntegerField(null=True, blank=True, help_text='Total rating of the event')
    count_rating = models.IntegerField(null=True, blank=True, help_text='Number of ratings of the event')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the event was created')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL,  related_name='events', null=True, blank=True, help_text='Place where the event is taking place')
    participants = models.ManyToManyField(User200, related_name='participated_events', help_text='Users participating in the event')
    reviewers = models.ManyToManyField(User200, through='EventReview', related_name='event_reviews', help_text='Users who have reviewed the event')

    def __str__(self):
        return self.name


class EventReview(models.Model):
    """
    Stores a single event review entry, related to :model:`main.Event`, :model:`main.User200`.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, help_text='The event being reviewed')
    user = models.ForeignKey(User200, on_delete=models.CASCADE, null=True, blank=True, help_text='The user who is providing the review')
    comment = models.TextField(null=True, blank=True, help_text='Comment provided by the user')
    created_at = models.DateTimeField(null=True, blank=True, help_text='Timestamp when the review was created')


class EventUser(models.Model):
    """
    Stores a single event user entry, related to :model:`main.Event`, :model:`main.User200`.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, help_text='The event being reviewed')
    user = models.ForeignKey(User200, on_delete=models.CASCADE, null=True, blank=True, help_text='The user who is providing the review')
    status = models.CharField(max_length=255, choices=[('interested', 'Interested'), ('going', 'Going'), ('attended', 'Attended')], help_text='The status of the user in the event. Choices are "interested", "going", and "attended"')
    created_at = models.DateTimeField(null=True, blank=True, help_text='Timestamp when the user joined the event')
    rating = models.IntegerField(null=True, blank=True, help_text='Rating provided by the user')

    class Meta:
        unique_together = ('event', 'user')


class Notification(models.Model):
    """
    Stores a single notification entry, related to :model:`main.NotificationType`, :model:`main.User200`.
    """
    notification_id = models.AutoField(primary_key=True, help_text='The unique identifier of the notification')
    user = models.ForeignKey(User200, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, help_text='The user receiving the notification')
    from_id = models.IntegerField(null=True, blank=True, help_text='The ID of the sender (user or organization)')
    from_type = models.CharField(max_length=255, choices=[('user', 'User'), ('organization', 'Organization')], help_text='The type of the sender. Choices are "user" and "organization"')
    message = models.TextField(null=True, blank=True, help_text='Message of the notification')
    notification_type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True, blank=True, help_text='Type of the notification')
    status = models.CharField(max_length=255, choices=[('unread', 'Unread'), ('read', 'Read')], help_text='The status of the notification. Choices are "unread" and "read"')
    created_at = models.DateTimeField(null=True, blank=True, help_text='Timestamp when the notification was created')

    def __str__(self):
        return f"Notification {self.notification_id} to {self.user}"

class OrganizationUser(models.Model):
    """
    Stores a single organization user entry, related to :model:`main.Organization`, :model:`main.User200`.
    """
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, help_text='The organization the user is associated with')
    user = models.ForeignKey(User200, on_delete=models.CASCADE, null=True, blank=True, help_text='The user who is associated with the organization')
    role = models.CharField(max_length=255, choices=[('member', 'Member'), ('follower', 'Follower')], help_text='The role of the user in the organization. Choices are "member" and "follower"')
    join_date = models.DateField(null=True, blank=True, help_text='Date when the user joined the organization')

    class Meta:
        unique_together = ('org', 'user')


class StudentOrg(models.Model):
    """
    Stores a single student organization entry, related to :model:`main.Faculty`.
    """
    org = models.OneToOneField(Organization, on_delete=models.CASCADE, null=True, blank=True, help_text='The organization associated with the student organization')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty', null=True, blank=True, help_text='The faculty associated with the student organization')