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
            def get_friend():
                offset = randint(0, 9)
                r = requests.get("https://api.vk.com/method/friends.get", params={'user_id':user_id, "v":5.122 ,'count': 5, "offset":offset, "access_token":TOKEN})
                response = r.json()

                friends_resp = response['response']['items']
                friends_list = []

                for friend in friends_resp:
                    friends_list.append(f'https://vk.com/id{friend}')

                return friends_list

            friends = get_friend()

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
            pass
    else:
        return render(request, 'redirect.html')