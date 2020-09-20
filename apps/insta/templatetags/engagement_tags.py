from django import template
from insta.models import InstagramFollower


register = template.Library()

@register.simple_tag
def get_rate(comment_count, like_count):
    total_followers = InstagramFollower.objects.all().count()

    if comment_count == '':
        comment_count = 0

    if like_count == '':
        like_count = 0
        
    eng_rate = ((int(comment_count) + int(like_count))/total_followers)*100
    return str(round(eng_rate, 2))