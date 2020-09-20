import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from django.conf import settings

from users.models import Notification
from .models import InstagramUserAnalytics, LinkedFbInfo, InstagramFollowing, InstagramFollower, TrackFollower, InstagramMedia, InstagramCarouselMedia

from InstagramAPI import InstagramAPI


def get_token():
    response = requests.get('https://www.instagram.com/oauth/authorize/?client_id=123&redirect_uri=http://127.0.0.1:8000/insta&response_type=token')
    return response

def get_media(tkn):
    response = requests.get('https://api.instagram.com/v1/self/media/recent?access_token=2016904458.123.123'+tkn)
    return response

def instagram_login(username, password):
    try:
        api = InstagramAPI(username, password)
        res = api.login()
        if res:
            return api
        else:
            return {"error" : "Invalid credentials"}
    except:
        return {"error" : "Invalid credentials"}

def get_insta_followers_list(api):
    follower_users = []
    api.getSelfUserFollowers()
    result = api.LastJson
    for user in result['users']:
        follower_users.append({'pk':user['pk'], 'username':user['username']})
    return follower_users

def get_insta_following_list(api):
    following_users = []
    api.getSelfUsersFollowing() # Get users which you are following
    result = api.LastJson
    for user in result['users']:
        following_users.append({'pk':user['pk'], 'username':user['username']})
    return following_users

def create_insta_following_list():
    username = settings.INSTA_USERNAME
    password = settings.INSTA_PASSWORD

    api = instagram_login(username, password)
    try:
        if api.get('error'):
            return api.get('error')
    except:
        pass
    # api.getSelfUsersFollowing()
    # result = api.LastJson

    result = api.getTotalSelfFollowings()

    count = 0
    for user in result:
        count += 1
        InstagramFollowing.objects.create(
            user_id = 1,
            insta_pk        = user['pk'],
            insta_username  = user['username'],
            insta_full_name = user['full_name'],
            is_private      = user['is_private'],
            profile_pic_url = user['profile_pic_url'],
            is_verified     = user['is_verified'])

    print("Total {} objects created.",format(count))
    return True


def create_insta_follower_list():
    username = settings.INSTA_USERNAME
    password = settings.INSTA_PASSWORD

    api = instagram_login(username, password)
    try:
        if api.get('error'):
            return api.get('error')
    except:
        pass

    # api.getSelfUserFollowers()
    # result = api.LastJson

    result = api.getTotalSelfFollowers()

    count = 0
    for user in result:
        count += 1
        InstagramFollower.objects.create(
            user_id = 1,
            insta_pk        = user['pk'],
            insta_username  = user['username'],
            insta_full_name = user['full_name'],
            is_private      = user['is_private'],
            profile_pic_url = user['profile_pic_url'],
            is_verified     = user['is_verified'])

    print("Total {} objects created.".format(count))
    return True

def get_insta_analytics():
    data = ""
    data+="[+] Insta Analytics [+] \n-------------[ SocAnt ]------------"

    # Get Last Object
    insta_ana = InstagramUserAnalytics.objects.all().last()
    following_user = InstagramFollowing.objects.filter(user_id=1)

    data+="\n[+] Total Followers : " + str(insta_ana.total_followers)
    data+="\n[+] Total Following : " + str(insta_ana.total_following)
    data+="\n[+] Is_private : " + str(insta_ana.is_private)
    data+="\n[+] Total Media Count : " + str(insta_ana.media_count)
    data+="\n[+] Private Account(Following) : " + str(following_user.filter(is_private = True).count())
    data+="\n[+] Last Updated_at   : " + insta_ana.last_updated_at.strftime("%d/%m/%Y, %H:%M:%S")
    return data

def update_insta_analytics():
    try:
        username = settings.INSTA_USERNAME
        password = settings.INSTA_PASSWORD

        api = instagram_login(username, password)
        try:
            if api.get('error'):
                return api.get('error')
        except:
            pass

        api.getSelfUsernameInfo()
        result = api.LastJson
        create_insta_analytic(result)

        # Find Out new followers/unfollowers
        api.getSelfUserFollowers()
        follower_result = api.LastJson
        current_status  = detect_new_follow_unfollow(follower_result)

        create_notification("Successfully Synched")
        return current_status
    except Exception as e:
        print(str(e))
        return "There is some issue while syncing your Insta data. Error : " + str(e)

def create_insta_analytic(result):
    try:
        full_name       = result['user']['full_name']
        profile_pic_url = result['user']['profile_pic_url']
        followers       = result['user']['follower_count']
        following       = result['user']['following_count']
        media_count     = result['user']['media_count']

        insta_pk        = result['user']['pk']
        insta_uname     = result['user']['username']
        profile_pic_url = result['user']['profile_pic_url']
        profile_pic_id  = result['user']['profile_pic_id']
        biography       = result['user']['biography']
        is_private      = result['user']['is_private']

        profile_pic_320 = result['user']['hd_profile_pic_versions'][0]['url']
        profile_pic_640 = result['user']['hd_profile_pic_versions'][1]['url']
        profile_pic_full= result['user']['hd_profile_pic_url_info']['url']


        fb_id      = result['user']['linked_fb_info']['linked_fb_user']['id']
        fb_name    = result['user']['linked_fb_info']['linked_fb_user']['name']
        fb_valid   = result['user']['linked_fb_info']['linked_fb_user']['is_valid']

        # Create FB LinkedFbInfo
        linked_fb = LinkedFbInfo.objects.create(
            fb_id   = fb_id,
            name    = fb_name,
            is_valid= fb_valid)

        InstagramUserAnalytics.objects.create(
            user_id  = 1, 
            linked_fb_info = linked_fb,
            total_followers = followers,
            total_following = following,
            total_likes_get = 1,
            total_liked     = 1,
            media_count     = media_count,
            insta_pk        = insta_pk,
            insta_full_name = full_name,
            insta_username  = insta_uname,
            profile_pic_url = profile_pic_url,
            profile_pic_id  = profile_pic_id,
            is_private      = is_private,
            biography       = biography,
            hd_profile_pic_versions_320 = profile_pic_320,
            hd_profile_pic_versions_640 = profile_pic_640,
            hd_profile_pic_url_info = profile_pic_full
        )
        return True
    except Exception as e:
        print(str(e))
        return False


def create_notification(message):
    Notification.objects.create(message=message)

def my_insta_details():
    if InstagramUserAnalytics.objects.filter(user_id=1).exists():
        insta_ana = InstagramUserAnalytics.objects.all().last()
        data = ""
        data+="[+] My Insta Details [+] \n-------------[ SocAnt ]------------"
        data+="\nID : "+ insta_ana.insta_pk
        data+="\nUsername : "+ insta_ana.insta_username
        data+="\nFull Name : "+ insta_ana.insta_full_name
        data+="\nIs Private : "+ str(insta_ana.is_private) ##Bool True/False
        data+="\nBio -->\n"+ insta_ana.biography
        return data
    else:
        return "Please update the Insta then try to fetch"


def detect_new_follow_unfollow(follower_result):

    """
        Long Function it is :-
        ----------------------
        Features it should return :
        1) Number of New Followers
        2) Number of Unfollowers
        3) If someone changes DP : Done
        4) If someone changes From private to public : Done
        5) If someone changes username : Done
        6) If someone changes Fullname : Done
    """
    data = ""
    data+="[+] New Changes In Insta [+] \n-------------[ SocAnt ]------------"

    for user in follower_result['users']:
        try:
            instance = InstagramFollower.objects.get(insta_pk  = user['pk'])

            # Check if username is changed from previous
            if instance.insta_username != user['username']:
                data+="\n=> " + instance.insta_full_name + " changed username to : " + user['username']
                instance.insta_username = user['username']

            # Check if full_name is changed from previous
            if instance.insta_full_name != user['full_name']:
                data+="\n=> " + instance.insta_full_name + " changed full_name to : " + user['full_name']
                instance.insta_full_name = user['full_name']

            # Check if is_private is changed from previous
            if instance.is_private != user['is_private']:
                data+="\n=> " + instance.is_private + " changed is_private to : " + str(user['is_private'])
                instance.is_private = user['is_private']

            # Check if profile_pic_url is changed from previous
            if check_if_dp_changed(instance.profile_pic_url, user['profile_pic_url']):
                data+="\n=> " + instance.insta_full_name + " changed DP"
                instance.profile_pic_url = user['profile_pic_url']

            # Check if is_verified is changed from previous
            if instance.is_verified != user['is_verified']:
                data+="\n=> " + instance.insta_full_name + " changed verified"
                instance.is_verified = user['is_verified']
            instance.save()

        except:
            pass
            # instace = InstagramFollower.objects.create(
            #     user_id         = 1,
            #     insta_pk        = user['pk'],
            #     insta_full_name = user['full_name'],
            #     is_private      = user['is_private'],
            #     profile_pic_url = user['profile_pic_url'],
            #     is_verified     = user['is_verified'],
            #     insta_username  = user['username'])
    return data


def check_if_dp_changed(local_pic1, new_pic2):
    url1 = local_pic1.split('=')[0].split('/')[-1]
    url2 = new_pic2.split('=')[0].split('/')[-1]
    if url1 == url2:
        return False
    else:
        return True

def get_tracked_accounts():
    tracked = TrackFollower.objects.all()
    data = ""
    data+="[+] My Tracked Accounts [+] \n-------------[ SocAnt ]------------"
    for track in tracked:
        data+="\nUsername : "+ track.track_insta.insta_username
        data+="\nFull Name : "+ track.track_insta.insta_full_name
        data+="\nIs active : "+ str(track.tracker_active)
        data+="\n----------------------------------------"
    return data

def add_new_to_track(username):
    try:
        # Check if the username is in your following list or not
        if InstagramFollowing.objects.filter(insta_username=username).exists():
            # Check if the username is already in Tracking or not
            track_acc = InstagramFollowing.objects.get(insta_username=username)

            # if TrackFollower.objects.filter

            TrackFollower.objects.create(
                            tracked_by_id = 1,
                            track_insta = track_acc)
        else:
            return "{} username is not found in your following list.".format(username)
        return "[+] Added Successfully to Track List \n - h4pPy h4cKing :v -"
    except Exception as e:
        return str(e)

def view_dp_of_account(username):
    try:
        url     = 'https://www.instadp.com/fullsize/'+username
        page    = requests.get(url)
        time.sleep(5.0)
        soup    = BeautifulSoup(page.text, 'html.parser')
        time.sleep(2.0)
        img_tag = soup.find_all("img", class_="picture")[0]
        img_url = img_tag.get('src')
        return str(img_url)
    except Exception as e:
        return str(e)


def create_my_post_media():
    try:
        username = settings.INSTA_USERNAME
        password = settings.INSTA_PASSWORD

        api = instagram_login(username, password)
        try:
            if api.get('error'):
                return api.get('error')
        except:
            pass

        # api.getTotalSelfFollowers()
        # import pdb; pdb.set_trace()
        result = api.getTotalSelfUserFeed()

        count = 0
        for post in result:

            # Check if that post id is in db or not
            ## TODO

            
            count += 1
            try:
                print("Not corousal")
                media_url     = post['image_versions2']['candidates'][0]['url']
                comment_count = post['comment_count']
                like_count    = post['like_count']
                caption       = post['caption']['text']

                uploaded_at   = datetime.fromtimestamp(post['taken_at'])

                InstagramMedia.objects.create(
                        user_id         = 1,
                        media_url       = media_url,
                        comment_count   = comment_count,
                        like_count      = like_count,
                        uploaded_at     = uploaded_at,
                        caption         = caption)

            except:
                print("corousal")

                uploaded_at   = datetime.fromtimestamp(post['taken_at'])

                insta_media = InstagramMedia.objects.create(
                        user_id         = 1,
                        comment_count   = post['comment_count'],
                        like_count      = post['like_count'],
                        uploaded_at     = uploaded_at,
                        caption         = post['caption']['text'])

                for media in post['carousel_media']:
                    carosal_media = InstagramCarouselMedia.objects.create(
                        media_url   = media['image_versions2']['candidates'][0]['url']
                        )
                    insta_media.carousel.add(carosal_media)


        print("Total {} objects created.",format(count))
        return True
    except Exception as e:
        print(str(e))
        return False