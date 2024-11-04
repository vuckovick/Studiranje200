from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
from django.utils import timezone
import json

class User200TestCase(TestCase):
    def setUp(self):
        faculty = Faculty.objects.create(
        name="Engineering",
        city="Test City",
        tag="ENG"
        )
    
        # Create a User200 instance with a hashed password
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser").update(
            first_name="Test",
            last_name="User",
            full_name="Test User",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="regular",
            unread_notifications=0
        )

        self.user = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser2").update(
            first_name="Test2",
            last_name="User2",
            full_name="Test User2",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="admin",
            unread_notifications=0
        )

        NotificationType.objects.create(name="become_organizer", id=6)

    def test_successful_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        self.assertContains(response, 'testuser')
        self.assertRedirects(response, reverse('index'))

    def test_unsuccessful_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertNotContains(response, 'testuser')

    def test_successful_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertNotContains(response, 'testuser')
        self.assertRedirects(response, reverse('index'))

    def test_my_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my-profile'))
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Test City')
        self.assertContains(response, 'Engineering')
        self.assertContains(response, 'https://instagram.com/testuser')
        self.assertContains(response, 'This is a test bio.')

    def test_edit_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-profile'), data={
            'first_name': 'New',
            'last_name': 'Name',
            'form_type': 'profile',
            'username': 'testuser',
            'date_birth': timezone.now().date(),
            'instagram': 'https://instagram.com/testuser',
            'email': 'test@gmail.com',
            'bio': 'This is a new bio.'

        }, follow=True)
        self.assertContains(response, 'New Name')
        self.assertNotContains(response, 'Test User')
        self.assertContains(response, 'This is a new bio.')
        self.assertNotContains(response, 'This is a test bio.')

    def test_change_password(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-profile'), data={
            'form_type': 'password',
            'curr_password': 'testpassword',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }, follow=True)
        self.assertTrue(User200.objects.filter(username='testuser').first().check_password('newpassword'))

    def test_wrong_password(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-profile'), data={
            'form_type': 'password',
            'curr_password': 'wrongpassword',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }, follow=True)
        self.assertFalse(User200.objects.filter(username='testuser').first().check_password('newpassword'))

    def test_non_matching_passwords(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-profile'), data={
            'form_type': 'password',
            'curr_password': 'testpassword',
            'password1': 'newpassword',
            'password2': 'newpassword2'
        }, follow=True)
        self.assertFalse(User200.objects.filter(username='testuser').first().check_password('newpassword'))

    def test_profile_view(self):
        response = self.client.get(reverse('profile_view', args=['testuser']))
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Test City')
        self.assertContains(response, 'Engineering')
        self.assertContains(response, 'https://instagram.com/testuser')
        self.assertContains(response, 'This is a test bio.')

    def test_register(self):
        response = self.client.post(reverse('register'), data={
            'fullname': 'New User',
            'dob': '2000-01-01',
            'place': Place.objects.create(
                name="Test Location",
                description="This is a test location.",
                working_hours="8-16",
                address="Test Address",
                place_type=PlaceType.objects.create(
                    name="Test Place Type"
                ),
                picture="placeholder.jpg",
                total_rating=0,
                count_rating=0,
                google_maps_url="https://maps.google.com",
                website_url="https://example.com"
            ).place_id,
            'faculty': Faculty.objects.create(
                name="Engineering",
                city="Test City",
                tag="ENG"
            ).faculty_id,
            'gender': 'M',
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newemail@example.com'
        }, follow=True)
        self.assertContains(response, 'New User')

    def test_become_org(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-profile'), data={
            'form_type': 'become_org',
        }, follow=True)
        self.assertTrue(Notification.objects.filter(user=User200.objects.get(username='testuser2'), notification_type=NotificationType.objects.get(name='become_organizer')).exists())

class Event200TestCase(TestCase):
    def setUp(self):
        faculty = Faculty.objects.create(
        name="Engineering",
        city="Test City",
        tag="ENG"
        )

        NotificationType.objects.create(
            id=7,
            name="new_event"
        )

                
    
        # Create a User200 instance with a hashed password
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser").update(
            first_name="Test",
            last_name="User",
            full_name="Test User",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="regular",
            unread_notifications=0
        )

        org = Organization.objects.create(
                name="Test Organization",
                description="This is a test organization.",
                picture="placeholder.jpg",
                total_rating=0,
                count_rating=0,
                created_at=timezone.now()
            )

        event = Event.objects.create(
            name="Test Event",
            description="This is a test event.",
            date=timezone.now().date(),
            time=timezone.now().time(),
            org= org,
            status="published",
            event_type=EventType.objects.create(
                name="Test Event Type"
            ),
            picture="placeholder.jpg",
            total_rating=0,
            count_rating=0,
            place=Place.objects.create(
                name="Test Location",
                description="This is a test location.",
                working_hours="8-16",
                address="Test Address",
                place_type=PlaceType.objects.create(
                    name="Test Place Type"
                ),
                picture="placeholder.jpg",
                total_rating=0,
                count_rating=0,
                google_maps_url="https://maps.google.com",
                website_url="https://example.com"
            )
        )

        OrganizationUser.objects.create(
            org=org,
            user=User200.objects.get(username="testuser"),
            role="member",
            join_date=timezone.now()
        )

        EventUser.objects.create(
            event=event,
            user=User200.objects.get(username="testuser"),
            status="interested",
            created_at=timezone.now()
        )

    def test_event_details(self):
        eventid = Event.objects.get(name="Test Event").event_id
        response = self.client.get(reverse('event_details', args=[eventid]))
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'This is a test event.')
        self.assertContains(response, 'Test Organization')
        self.assertContains(response, 'Test Event Type')

    
    def test_events(self):
        response = self.client.get(reverse('events'))
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'Test Event Type')

    def test_create_event(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('events'), data={
            'form_type': 'event',
            'title': 'New Event',
            'description': 'This is a new event.',
            'date': '2021-12-31',
            'time': '12:00',
            'event_type': EventType.objects.get(name="Test Event Type"),
            'place': Place.objects.get(name="Test Location").place_id
        }, follow=True)
        self.assertContains(response, 'Test Event')

    def test_filter_events(self):
        response = self.client.post(reverse('events'), data={
            'form_type': 'filter',
            'datefrom': '2021-01-01',
            'dateto': '2022-12-31',
        })
        self.assertContains(response, 'Test Event')

    def test_commenting(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('event_details', args=[Event.objects.get(name="Test Event").event_id]), data={
            'comment': 'This is a test comment.',
            'rating': '5'
        }, follow=True)
        self.assertTrue(EventReview.objects.filter(event=Event.objects.get(name="Test Event"), user=User200.objects.get(username="testuser"), comment="This is a test comment.").exists())

class OrganizationTestCase(TestCase):
    def setUp(self):
        
        faculty = Faculty.objects.create(
        name="Engineering",
        city="Test City",
        tag="ENG"
        )
    
        # Create a User200 instance with a hashed password
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser").update(
            first_name="Test",
            last_name="User",
            full_name="Test User",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="regular",
            unread_notifications=0
        )
        
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            email="testuser2@example.com",
        )

        User200.objects.filter(username="testuser2").update(
            first_name="Test2",
            last_name="User2",
            full_name="Test User2",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="organizer",
            unread_notifications=0
        )
        
        org = Organization.objects.create(
                name="Test Organization",
                description="This is a test organization.",
                picture="placeholder.jpg",
                total_rating=0,
                count_rating=0,
                created_at=timezone.now()
        )

        OrganizationUser.objects.create(org = org, user = User200.objects.get(username="testuser2"), role = "member", join_date = timezone.now())
    
    def test_organization_details(self):
        orgid = Organization.objects.get(name="Test Organization").org_id
        response = self.client.get(reverse('organization-details', args=[orgid]))
        self.assertContains(response, 'Test Organization')
        self.assertContains(response, 'This is a test organization.')

    def test_organizations(self):
        response = self.client.get(reverse('organizations'))
        self.assertContains(response, 'Test Organization')

    def test_create_organization(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('organizations'), data={
            'form_type': 'organization',
            'name': 'New Organization',
            'description': 'This is a new organization.'
        }, follow=True)
        self.assertContains(response, 'New Organization')

    def test_filter_organizations(self):
        response = self.client.post(reverse('organizations'), data={
            'form_type': 'filter1',
            'name': 'Test Organization',
            'order': 'newest'
        })
        self.assertContains(response, 'Test Organization')

class LocationTestCase(TestCase):
    def setUp(self):
        faculty = Faculty.objects.create(
        name="Engineering",
        city="Test City",
        tag="ENG"
        )
    
        # Create a User200 instance with a hashed password
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser").update(
            first_name="Test",
            last_name="User",
            full_name="Test User",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="regular",
            unread_notifications=0
        )

        place=Place.objects.create(
                name="Test Location",
                description="This is a test location.",
                working_hours="8-16",
                address="Test Address",
                place_type=PlaceType.objects.create(
                    name="Test Place Type"
                ),
                picture="placeholder.jpg",
                total_rating=0,
                count_rating=0,
                google_maps_url="https://maps.google.com",
                website_url="https://example.com"
            )
    
    def test_location_details(self):
        placeid = Place.objects.get(name="Test Location").place_id
        response = self.client.get(reverse('location-details', args=[placeid]))
        self.assertContains(response, 'Test Location')
        self.assertContains(response, 'This is a test location.')

    def test_locations(self):
        response = self.client.get(reverse('locations'))
        self.assertContains(response, 'Test Location')

    def test_create_location(self):
        self.client.login(username='testuser', password='testpassword')
    
        # Create PlaceType instance outside the data dictionary
        place_type_instance = PlaceType.objects.create(name="Test Place Type 2")
        
        # Use the ID of the PlaceType instance in the POST data
        response = self.client.post(reverse('locations'), data={
            'form_type': 'location',
            'name': 'New Location',
            'description': 'This is a new location.',
            'working_hours': '8-16',
            'address': 'New Address',
            'type': place_type_instance,  # Assign the ID of the instance
            'google_maps': 'https://maps.google.com',
        }, follow=True)
        
        self.assertContains(response, 'New Location')

    def test_filter_locations(self):
        response = self.client.post(reverse('locations'), data={
            'form_type': 'filter1',
            'name': 'Test Location',
            'order': 'newest'
        })
        self.assertContains(response, 'Test Location')

class NotificationTestCase(TestCase):
    def setUp(self):
        faculty = Faculty.objects.create(
        name="Engineering",
        city="Test City",
        tag="ENG"
        )
    
        # Create a User200 instance with a hashed password
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        # Update the User200 instance with additional fields
        User200.objects.filter(username="testuser").update(
            first_name="Test",
            last_name="User",
            full_name="Test User",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="admin",
            unread_notifications=0
        )

        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            email="testuser2@example.com",
        )

        User200.objects.filter(username="testuser2").update(
            first_name="Test2",
            last_name="User2",
            full_name="Test User2",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="organizer",
            unread_notifications=0
        )

        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
            email="testuser3@example.com",
        )

        User200.objects.filter(username="testuser3").update(
            first_name="Test3",
            last_name="User3",
            full_name="Test User3",
            date_birth=timezone.now().date(),
            gender="M",
            city="Test City",
            faculty=faculty,
            instagram_link="https://instagram.com/testuser",
            profile_picture="placeholder.jpg",
            bio="This is a test bio.",
            role="regular",
            unread_notifications=0
        )

        org = Organization.objects.create(
            name="Test Organization",
            description="This is a test organization.",
            picture="placeholder.jpg",
            total_rating=0,
            count_rating=0,
            created_at=timezone.now()
        )

        OrganizationUser.objects.create(
            org=org,
            user=User200.objects.get(username="testuser2"),
            role="admin",
            join_date=timezone.now()
        )

        Notification.objects.create(
            user=User200.objects.get(username="testuser"),
            from_id=User200.objects.get(username="testuser2").id,
            from_type="organization",
            message="Test notification",
            notification_type=NotificationType.objects.create(
                name="connection_request"
            ),
            status="unread",
            created_at=timezone.now()
        )

        Notification.objects.create(
            user=User200.objects.get(username="testuser3"),
            from_id=User200.objects.get(username="testuser2").id,
            from_type="organization",
            message="Test notification2",
            notification_type=NotificationType.objects.filter(name="connection_request").first(),
            status="unread",
            created_at=timezone.now()
        )

        NotificationType.objects.create(
            name="standard"
        )

        Connection.objects.create(
            follower=User200.objects.get(username="testuser2"),
            followee=User200.objects.get(username="testuser"),
            follow_date=timezone.now(),
            status="pending"
        )

        Connection.objects.create(
            follower=User200.objects.get(username="testuser2"),
            followee=User200.objects.get(username="testuser3"),
            follow_date=timezone.now(),
            status="pending"
        )

    def send_connection_request(self):
        response = self.client.post(reverse('send_connection_request'), json.dumps({
            'followeeId': self.recipient.id
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Connection.objects.filter(follower=self.user1, followee=self.recipient).exists())
        self.assertTrue(Notification.objects.filter(user=self.recipient, notification_type=self.notification_type).exists())
    
    def test_accept_conn_request(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Now make the post request as the authenticated user
        response = self.client.post(reverse('accept_conn_request'), json.dumps({
            'notification_id': Notification.objects.get(message="Test notification").notification_id
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Connection.objects.filter(follower=self.user2, followee=self.user, status="accepted").exists())

    def test_decline_conn_request(self):
        self.client.login(username='testuser3', password='testpassword')
        
        # Now make the post request as the authenticated user
        response = self.client.post(reverse('decline_conn_request'), json.dumps({
            'notification_id': Notification.objects.get(message="Test notification2").notification_id
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Connection.objects.filter(follower=self.user2, followee=self.user3, status="declined").exists())

class AcceptJoinRequestTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.notification_type = NotificationType.objects.create(name="join_request")
        self.notification_type = NotificationType.objects.create(name="standard", id=4)
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="želi da se učlani u Test Organization",
            notification_type=self.notification_type,
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_accept_join_request(self):
        # Send POST request to accept join request
        response = self.client.post(reverse('accept_join_request'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(OrganizationUser.objects.filter(user=self.user, org=self.org).exists())
        self.assertTrue(Notification.objects.filter(message__contains=f"vas je prihvatio/la u {self.org}").exists())


class AcceptOrgRequestTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.notification_type_join_request = NotificationType.objects.create(name="join_request")
        self.notification_type_standard = NotificationType.objects.create(name="standard", id=4)
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="želi da se učlani u Test Organization",
            notification_type=self.notification_type_join_request,
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_accept_org_request(self):
        # Send POST request to accept organization request
        response = self.client.post(reverse('accept_org_request'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertEqual(self.user.role, 'organizer')
        self.assertTrue(Notification.objects.filter(message__contains="je odobrio tvoj zahtev. Sada si organizator!").exists())

class AcceptEventRequestTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.event = Event.objects.create(name="Test Event", description="Test Description")
        self.notification_type_join_request = NotificationType.objects.create(name="join_request")
        self.notification_type_standard = NotificationType.objects.create(name="standard", id=4)
        
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Event",
            notification_type=self.notification_type_join_request,
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_accept_event_request(self):
        # Send POST request to accept event request
        response = self.client.post(reverse('accept_event_invite'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(EventUser.objects.filter(user=self.user, event=self.event).exists())

class DeclineEventRequestTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.event = Event.objects.create(name="Test Event", description="Test Description")
        self.notification_type_join_request = NotificationType.objects.create(name="join_request")
        self.notification_type_standard = NotificationType.objects.create(name="standard", id=4)
        
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Event",
            notification_type=self.notification_type_join_request,
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_decline_event_request(self):
        # Send POST request to decline event request
        response = self.client.post(reverse('decline_event_invite'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(EventUser.objects.filter(user=self.user, event=self.event).exists())

class DeclineJoinRequestTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.notification_type_join_request = NotificationType.objects.create(name="join_request")
        self.notification_type_standard = NotificationType.objects.create(name="standard", id=4)
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="želi da se učlani u Test Organization",
            notification_type=self.notification_type_join_request,
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_decline_join_request(self):
        # Send POST request to decline join request
        response = self.client.post(reverse('decline_join_request'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(OrganizationUser.objects.filter(user=self.user, org=self.org).exists())

class DeleteOneNotificationTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Notification",
            notification_type=NotificationType.objects.create(name="standard"),
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_delete_one_notification(self):
        # Send POST request to delete one notification
        response = self.client.post(reverse('delete_one_notification'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(Notification.objects.filter(user=self.user, notification_id=self.notification.notification_id).exists())
    
class DeleteAllNotificationsTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Notification",
            notification_type=NotificationType.objects.create(name="standard"),
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_delete_all_notifications(self):
        # Send POST request to delete all notifications
        response = self.client.post(reverse('delete_all_notifications'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(Notification.objects.filter(user=self.user).exists())

class MarkAllNotificationsReadTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Notification",
            notification_type=NotificationType.objects.create(name="standard"),
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_mark_all_notifications_read(self):
        # Send POST request to mark all notifications as read
        response = self.client.post(reverse('mark_all_notifications_read'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Notification.objects.filter(user=self.user, status="read").exists())

class MarkOneReadTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.notification = Notification.objects.create(
            user=self.user,
            from_id=self.user.id,
            from_type="user",
            message="Test Notification",
            notification_type=NotificationType.objects.create(name="standard"),
            status="unread"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_mark_one_read(self):
        # Send POST request to mark one notification as read
        response = self.client.post(reverse('mark_one_read'), json.dumps({
            'notification_id': self.notification.notification_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertEqual(Notification.objects.get(notification_id=self.notification.notification_id).status, 'read')

class MarkInterestedTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.event = Event.objects.create(name="Test Event", description="Test Description")
        self.client.login(username='testuser', password='testpassword')

    def test_mark_interested(self):
        # Send POST request to mark event as interested
        response = self.client.post(reverse('mark_interested'), json.dumps({
            'event_id': self.event.event_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(EventUser.objects.filter(user=self.user, event=self.event, status="interested").exists())

class FollowOrganizationTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.client.login(username='testuser', password='testpassword')

    def test_follow_organization(self):
        # Send POST request to follow organization
        response = self.client.post(reverse('follow_organization'), json.dumps({
            'org_id': self.org.org_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(OrganizationUser.objects.filter(user=self.user, org=self.org, role="follower").exists())

class JoinOrganizationTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.client.login(username='testuser', password='testpassword')
        self.notification_type_join_organization = NotificationType.objects.create(name="join_organization", id=5)

    def test_join_organization(self):
        # Send POST request to join organization
        response = self.client.post(reverse('join_organization'), json.dumps({
            'org_id': self.org.org_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

class LeaveOrganizationTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.client.login(username='testuser', password='testpassword')
        self.notification_type_standard = NotificationType.objects.create(name="standard", id=4)

    def test_leave_organization(self):
        # Send POST request to leave organization
        response = self.client.post(reverse('leave_organization'), json.dumps({
            'org_id': self.org.org_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(OrganizationUser.objects.filter(user=self.user, org=self.org).exists())
        
class RemoveFollowerTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.user2 = User200.objects.create_user(username="testuser2", password="testpassword", role="user")
        Connection.objects.create(follower=self.user2, followee=self.user, status="accepted")
        Connection.objects.create(follower=self.user, followee=self.user2, status="accepted")
        self.client.login(username='testuser', password='testpassword')

    def test_remove_follower(self):
        # Send POST request to remove follower
        response = self.client.post(reverse('remove_followee'), json.dumps({
            'followee_id': self.user2.id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertFalse(Connection.objects.filter(follower=self.user2, followee=self.user).exists())
        self.assertFalse(Connection.objects.filter(follower=self.user, followee=self.user2).exists())

class InviteFollowersToParty(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.user2 = User200.objects.create_user(username="testuser2", password="testpassword", role="user")
        self.org = Organization.objects.create(name="Test Organization", description="Test Description")
        self.event = Event.objects.create(name="Test Event", description="Test Description", org=self.org)
        OrganizationUser.objects.create(org=self.org, user=self.user, role="member")
        OrganizationUser.objects.create(org=self.org, user=self.user2, role="follower")
        self.client.login(username='testuser', password='testpassword')
        NotificationType.objects.create(name="event_invite", id=2)

    def test_invite_followers_to_party(self):
        # Send POST request to invite followers to party
        response = self.client.post(reverse('invite_followers_to_party'), json.dumps({
            'event_id': self.event.event_id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Notification.objects.filter(user=self.user2, notification_type=NotificationType.objects.get(id=2)).exists())

class SendConnectionInvite(TestCase):
    def setUp(self):
        # Create test data
        self.user = User200.objects.create_user(username="testuser", password="testpassword", role="user")
        self.user2 = User200.objects.create_user(username="testuser2", password="testpassword", role="user")
        self.client.login(username='testuser', password='testpassword')
        notification_type = NotificationType.objects.create(name="connection_request")

    def test_send_connection_invite(self):
        # Send POST request to send connection invite
        response = self.client.post(reverse('send_connection_request'), json.dumps({
            'followeeId': self.user2.id
        }), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertTrue(Connection.objects.filter(follower=self.user, followee=self.user2, status="pending").exists())

