from django.shortcuts import render
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken
from django.contrib import sessions
import requests
from random import randint

def index(request):
   
    return render(request, 'index.html')



def profile(request):

    if request.user.is_authenticated:
        try:
           
            first_name = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['first_name']
            user_id = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['id']
            last_name = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['last_name']
            # bdate = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['bdate']
            # city = SocialAccount.objects.filter(user=request.user, provider='vk')[0].extra_data['city']['title']
            #allinfo = SocialAccount.objects.filter(user=request.user, provider='vk')
            #allinfo = SocialAccount.objects.filter(provider='vk')[0].extra_data
            #TOKEN = SocialToken.objects.filter(user=request.user, provider='vk')[0]
            TOKEN =  SocialToken.objects.filter(account__user=request.user, account__provider='vk')
            

            friends = get_friend(user_id, TOKEN)

            context = {
                'first_name': first_name,
                'last_name': last_name,
                # 'bdate': bdate,
                # 'city': city,
                'friends': friends,
                #'allinfo': allinfo,
            }
            return render(request, 'profile.html', context)
        except:
            return 'Ошибка'
    else:
        return render(request, 'redirect.html')


def get_friend(user_id, TOKEN):
    offset = randint(0, 15)
    friend_list_count = 5
    request_params = {
        'user_id': user_id, 
        'count': friend_list_count, 
        'offset': offset,
        'fields': 'photo_200',
        'v': 5.122 , 
        'access_token': TOKEN}
    try:
        r = requests.get("https://api.vk.com/method/friends.get", params=request_params)
        response = r.json()

        friends_resp = response['response']['items']
        friends_list = []

        for friend in friends_resp:
            #friends_list.append(f'https://vk.com/id{friend}')
            friend_profile = {
                'first_name': friend['first_name'],
                'last_name': friend['last_name'],
                'photo_200': friend['photo_200']
            }
            friends_list.append(friend_profile)
        return friends_list
    except:
        return 'Ошибка'


    