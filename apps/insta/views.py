from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InstagramUserAnalytics, TrackFollower, InstagramMedia

from .helpers import *

from InstagramAPI import InstagramAPI
from twilio.rest import Client
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.loader import get_template
from django.core.mail import EmailMessage

# Create your views here.
@login_required
def insta_index(request):
    data = {}
    data['medias'] = InstagramMedia.objects.filter(user=request.user)
    return render(request,'insta/insta_dashboard.html',data)


@login_required
def insta_profile(request):
    data = {}
    # update_insta_analytics()

    data['notifications'] =Notification.objects.filter(is_read=False)
    data['analytics'] = InstagramUserAnalytics.objects.filter(user=request.user).last()
    return render(request,'insta/my_insta_dashbaord.html',data)

@login_required
def update_insta_feed(request):
    try:
        update_insta_analytics()
        # pass
        return JsonResponse({'status':True,'message':'Successfully Updated!'})
    except Exception as e:
        return JsonResponse({'status':False,'message':str(e)})

@login_required
def insta_follower_list(request):
    data = {}

    follower_user = InstagramFollower.objects.filter(user=request.user)

    # If no object then create follower list first
    if not follower_user.exists():
        create_insta_follower_list()
    
    else:
        follower_user = InstagramFollower.objects.filter(user=request.user)

    data['private_profile_count'] = follower_user.filter(is_private = True).count()
    data['verified_profile_count'] = follower_user.filter(is_verified = True).count()
    data['follower_user_count'] = follower_user.count()

    page = request.GET.get('page', 1)

    paginator = Paginator(follower_user, 10)
    try:
        follower_user = paginator.page(page)
    except PageNotAnInteger:
        follower_user = paginator.page(1)
    except EmptyPage:
        follower_user = paginator.page(paginator.num_pages)

    data['follower_user'] = follower_user
    return render(request,'insta/insta_followers.html',data)


@login_required
def insta_following_list(request):
    data = {}

    following_user = InstagramFollowing.objects.filter(user=request.user)

    # If no object then create following list first
    if not following_user.exists():
        create_insta_following_list()
    else:
        following_user = InstagramFollowing.objects.filter(user=request.user)

    data['private_profile_count'] = following_user.filter(is_private = True).count()
    data['verified_profile_count'] = following_user.filter(is_verified = True).count()
    data['following_user_count'] = following_user.count()

    page = request.GET.get('page', 1)

    paginator = Paginator(following_user, 10)
    try:
        following_user = paginator.page(page)
    except PageNotAnInteger:
        following_user = paginator.page(1)
    except EmptyPage:
        following_user = paginator.page(paginator.num_pages)

    data['following_user'] = following_user
    return render(request,'insta/insta_following.html',data)


@login_required
def insta_tracked_accounts(request):
    data = {}
    data['tracked_user'] = TrackFollower.objects.filter(track_insta__user=request.user)
    return render(request,'insta/insta_tracked.html',data)


@csrf_exempt
def twilio(request):
    if request.method == 'POST':
        wsp_message = (request.POST.get('Body')).lower()

        media_provided = False
        account_sid = settings.ACCOUNT_SID
        auth_token  = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)

        if wsp_message == 'hi':
            body = """
                [+] *Welcome To Project SocAnt* [+]\n-----------------ヾ(＾-＾)ノ----------------
                \nVersion : 0.01
                \n- _Developed By D Ashwin_
                """
        
        elif wsp_message == 'help':
            body = """
                [+] Select one Option [+] \n-------------[ SocAnt ]------------
                \n1) Get Insta Analytics
                \n2) Update/Sync Insta Analytics Data
                \n3) My Insta Details
                \n4) My Tracked Accounts
                \n5) Add New Account to track
                \n6) View DP of any Insta account
                """
        elif wsp_message == '1':
            body = get_insta_analytics()
        
        elif wsp_message == '2':
            body = update_insta_analytics()
        
        elif wsp_message == '3':
            body = my_insta_details()

        elif wsp_message == '4':
            body = get_tracked_accounts()

        elif wsp_message == '5':
            body = "Reply with add:<username of insta>"

        elif wsp_message.startswith('add:'):
            account_username = wsp_message.split(':')[1]
            body = add_new_to_track(account_username)

        elif wsp_message == '6':
            body = "Reply with viewdp:<username of insta>"

        elif wsp_message.startswith('viewdp:'):
            account_username = wsp_message.split(':')[1]
            body = account_username
            pic_url = view_dp_of_account(account_username)
            media_provided = True
            media_url = pic_url
        else:
            body = "Invalid Choice... Please reply 'help' to see the option"

        # Check if body char limit exceeds 1600 Chars. 
        limit = 1500

        if len(body) > limit :
            n = limit
            chunked = [body[i:i+n] for i in range(0, len(body), n)]

            for chunk in chunked:
                message = client.messages.create(
                                    from_='whatsapp:+1415238886',
                                    body=chunk,
                                    to='whatsapp:'+settings.MY_PHONE)
        else:
            if media_provided == False:
                message = client.messages.create(
                                        from_='whatsapp:+14155238886',
                                        body=body,
                                        to='whatsapp:'+settings.MY_PHONE)
            else:
                message = client.messages.create(
                                        from_='whatsapp:+14155238886',
                                        body=body,
                                        media_url=media_url,
                                        to='whatsapp:'+settings.MY_PHONE)

        return HttpResponse("True")
    else:
        return HttpResponse("False")


# Webhook Error View : Later
# @csrf_exempt
# def twilio_errors(request):
#     if request.method == 'POST':
#         print("here")
#         return HttpResponse("True")
#     else:
#         print("here124")
#         return HttpResponse("Please Hit the POST request")


# Change status of tracked_user
@login_required
def update_tracker(request):
    try:
        # Request Data
        insta_pk        = request.POST.get('following_insta_id',None)
        tracker_active  = request.POST.get('tracker_active',None)

        # TrackFollower Object
        tracked  = TrackFollower.objects.get(track_insta__insta_pk = insta_pk)
        tracked.tracker_active = True if tracker_active == 'true' else False
        tracked.save()

        return JsonResponse({'status':True,'message':'Successfully Updated!'})
    except Exception as e:
        return JsonResponse({'status':False,'message':str(e)})


def sendmail(request):
    try:
        ctx = {
            "schedule_type"        : "test"
        }

        subject = "demo"

        message = get_template('email/demo.html').render(ctx)
        msg = EmailMessage(subject, message, to=('kewef44103@katamo1.com',),from_email='kewef44103@katamo1.com')
        msg.content_subtype = 'html'
        msg.send()
        print("Mail Sent Successfully")
        return HttpResponse("Sent mail")
    except Exception as e:
        print("Uh oh, We met error :",str(e))


@login_required
def insta_my_posts(request):
    data = {}

    create_my_post_media()
    return JsonResponse({'status':True,'message':'Successfully Updated!'})
    # follower_user = InstagramFollower.objects.filter(user=request.user)

    # If no object then create follower list first
    # if not follower_user.exists():
        # create_insta_follower_list()
    
    # else:
        # follower_user = InstagramFollower.objects.filter(user=request.user)


class DemoTestCase(APIView):

    def get(self, request):
        return Response(True, status=status.HTTP_200_OK)
