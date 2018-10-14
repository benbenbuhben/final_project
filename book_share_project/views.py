from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from book_share_app.models import Profile
from allauth.socialaccount.models import SocialAccount
import requests
import json


def home_view(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    profile = Profile.objects.filter(user_id__username=request.user.username)

    fb_account = SocialAccount.objects.filter(user_id__username=request.user.username)

    # We have the right social_account instance (i.e., table row). There has to be an easier way to grab the uid (i.e., the cell in that row)
    uid = list(fb_account.values('uid'))[0]['uid']
    extra_data = list(fb_account.values('extra_data'))[0]['extra_data']

    if not profile:

        endpoint = 'https://graph.facebook.com/{}?fields=picture'.format(uid)
        headers = {"Authorization": "Bearer 278758722745488|zgMN8ZoPRELH14yZO8TiQQNGgPM"}
        response = requests.get(endpoint, headers=headers).json()
        picture = response['picture']['data']['url']

        Profile.objects.create(
            user_id=request.user,
            username=request.user.username,
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            fb_id=uid,
            picture=picture,
        )

    return render(request, 'base/home.html')
