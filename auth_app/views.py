from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
import requests
from . import vk_utility

def index(request):
    if 'testcookie' not in request.COOKIES: # проверяем браузер пользователя на наличие куки от нашего приложения
        return render(request, 'auth_app/homePage2.html', ) # если куки не обнаружено значит пользователь зашел к нам в первый раз и направляем его на кнопку авторизации
    else:
        return redirect("auth_app/friends/") # если куки обнаружено - сразу перенаправляем пользователя на приложение авторизации
     
def friends(request):
    request_link = "https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=https://myvkauth.herokuapp.com/auth_app/friends/&display=page&scope=friends,offline&response_type=code"
    r = requests.get(url=request_link)
    current_url = r.build_absolute_uri() # записываем в переменную текущую ссылку
    code = current_url[-18:] # получаем код из ссылки
    report = vk_utility.auth(code)  # функция vk_utility.auth на входе получает код. при помощи кода получает доступ к списку друзей пользователя
                                    # и возвращает список из 5 друзей пользователя
    if 'testcookie' not in request.COOKIES: # проверяем бразуер пользователя на наличие куки из данного приложения
        response = HttpResponse(report)
        response.set_cookie('testcookie', 'VK_auth', max_age=60*60) # если кнопкуи не обнаружено - записываем куки в браузер
    else:
        response = HttpResponse(report)
    return response