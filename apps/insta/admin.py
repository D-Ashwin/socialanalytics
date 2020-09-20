from django.contrib import admin
from .models import InstagramUserAnalytics, TrackFollower, InstagramFollowing, InstagramFollower, InstagramMedia, InstagramCarouselMedia
from users.models import Notification


class InstagramFollowingAdmin(admin.ModelAdmin):
    search_fields = ("insta_username","insta_full_name")


class InstagramFollowerAdmin(admin.ModelAdmin):
    search_fields = ("insta_username","insta_full_name")


admin.site.register(InstagramUserAnalytics)
admin.site.register(InstagramFollowing, InstagramFollowingAdmin)
admin.site.register(InstagramFollower, InstagramFollowerAdmin)
admin.site.register(TrackFollower)
admin.site.register(Notification)
admin.site.register(InstagramMedia)
admin.site.register(InstagramCarouselMedia)