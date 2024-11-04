#Created by: 
#   Vanja Tomic 0289/21
#   Konstantin Vuckovic 0524/21
#   Vladimir Bogojevic 0387/21
#   Mihajlo Antonijevic 0382/21

from django.contrib import admin
from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('events/', events, name='events'),
    path('event-details/<int:event_id>/', event_details, name='event_details'),
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('locations/', locations, name='locations'),
    path('organizations/', organizations, name='organizations'),
    path('upload/', upload, name='upload'),
    path('my-profile/', my_profile, name='my-profile'),
    path('notifications/', notifications, name='notifications'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('organization-details/<int:org_id>/', organization_details, name='organization-details'),
    path('location-details/<int:place_id>/', location_details, name='location-details'),
    path('mark_interested/', mark_interested, name='mark_interested'),
    path('follow_organization/', follow_organization, name='follow_organization'),
    path('join_organization/', join_organization, name='join_organization'),
    path('leave_organization/', leave_organization, name='leave_organization'),
    path('accept_join_request/', accept_join_request, name='accept_join_request'),
    path('decline_join_request/', decline_join_request, name='decline_join_request'),
    path('accept_org_request/', accept_org_request, name='accept_org_request'),
    path('accept_conn_request/', accept_conn_request, name='accept_conn_request'),
    path('decline_conn_request/', decline_conn_request, name='decline_conn_request'),
    path('mark_all_read/', mark_all_read, name='mark_all_read'),
    path('mark_one_read/', mark_one_read, name='mark_one_read'),
    path('delete_one_notification/', delete_one_notification, name='delete_one_notification'),
    path('remove_followee', remove_followee, name='remove_followee'),
    path('update_mutual_connections', update_mutual_connections, name='update_mutual_connections'),
    path('notifications/mark_all_notifications_read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/delete_all_notifications/', delete_all_notifications, name='delete_all_notifications'),
    path('invite_followers_to_party/', invite_followers_to_party, name='invite_followers_to_party'),
    path('decline_event_invite/', decline_event_invite, name='decline_event_invite'),
    path('accept_event_invite/', accept_event_invite, name='accept_event_invite'),
    path('send_connection_request/', send_connection_request, name='send_connection_request'),

    path('<username>/', profile_view, name='profile_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)