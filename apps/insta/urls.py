from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.insta_index, name='insta-dashboard'),
    path('insta-profile', views.insta_profile, name='insta-profile'),
    path('insta-followers', views.insta_follower_list, name='insta-followers'),
    path('insta-following', views.insta_following_list, name='insta-following'),
    path('insta-tracked', views.insta_tracked_accounts, name='insta-tracked-accounts'),
    path('insta-my-posts', views.insta_my_posts, name='insta-my-posts'),
    path('insta-update', views.update_insta_feed, name='insta-update'),
    path('tracker-update/', views.update_tracker, name='tracker-update/'),
    path('twilio/', views.twilio, name='twilio'),
    # path('twilio-errors/', views.twilio_errors, name='twilio-errors'),
    path('sendmail', views.sendmail, name='sendmail'),

    # TestCase demo
    path('test/', views.DemoTestCase.as_view(), name='testcase-demo'),
]