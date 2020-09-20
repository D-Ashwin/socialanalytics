from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LinkedFbInfo(models.Model):
    fb_id   = models.CharField(max_length=255)
    name    = models.CharField(max_length=255)
    is_valid= models.BooleanField(default=True)
    def __str__(self):
        return str(self.name)

class InstagramUserAnalytics(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    linked_fb_info  = models.ForeignKey(LinkedFbInfo,on_delete=models.CASCADE, null=True)
    total_followers = models.IntegerField()
    total_following = models.IntegerField()
    total_likes_get = models.IntegerField()
    total_liked     = models.IntegerField()
    media_count     = models.IntegerField(default=0)

    insta_pk        = models.CharField(max_length=255)
    insta_username  = models.CharField(max_length=255)
    insta_full_name = models.CharField(max_length=255)
    profile_pic_url = models.CharField(max_length=255)
    profile_pic_id  = models.CharField(max_length=255)
    is_private      = models.BooleanField(default=True)
    biography       = models.CharField(max_length=355)
    hd_profile_pic_versions_320=models.CharField(max_length=255)
    hd_profile_pic_versions_640=models.CharField(max_length=255)
    hd_profile_pic_url_info=models.CharField(max_length=255)

    last_updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.insta_username)


class InstagramFollowing(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    insta_pk        = models.CharField(max_length=255)
    insta_username  = models.CharField(max_length=255)
    insta_full_name = models.CharField(max_length=255)
    profile_pic_url = models.CharField(max_length=255)
    is_private      = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    last_updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.insta_username)


class InstagramFollower(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    insta_pk        = models.CharField(max_length=255)
    insta_username  = models.CharField(max_length=255)
    insta_full_name = models.CharField(max_length=255)
    profile_pic_url = models.CharField(max_length=255)
    is_private      = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    last_updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.insta_username)

class TrackFollower(models.Model):
    tracked_by      = models.ForeignKey(User,on_delete=models.CASCADE) # It should be InstagramUserAnalytics
    track_insta     = models.ForeignKey(InstagramFollowing,on_delete=models.CASCADE)
    tracker_active  = models.BooleanField(default=True)

    def __str__(self):
        return str(self.tracked_by)


class InstagramCarouselMedia(models.Model):
    media_url       = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)


class InstagramMedia(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    media_url       = models.CharField(max_length=255, null=True, blank=True)
    comment_count   = models.CharField(max_length=255)
    like_count      = models.CharField(max_length=255)
    caption         = models.CharField(max_length=255)
    uploaded_at     = models.DateTimeField(blank=True, null=True)
    carousel        = models.ManyToManyField('InstagramCarouselMedia', related_name='carousel', blank=True)

    def __str__(self):
        return str(self.user.pk)
