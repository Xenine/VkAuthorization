from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import requests
from . import vk_utility

def index(request):
    if 'testcookie' not in request.COOKIES: # проверяем браузер пользователя на наличие куки от нашего приложения
        return render(request, 'auth_app/homePage2.html', ) # если куки не обнаружено значит пользователь зашел к нам в первый раз и направляем его на кнопку авторизации
    else:
        return redirect("https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=http://vk.com&display=page&scope=friends,offline&response_type=code") # если куки обнаружено - сразу перенаправляем пользователя на приложение авторизации
     
def login(request):
    #link = "https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=http://vk.com&display=page&scope=friends,offline&response_type=code"
    #r = requests.get(url=link)
    return redirect("https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=http://vk.com&display=page&scope=friends,offline&response_type=code")


def friends(request):
    #return render(request, 'auth_app/homePage2.html', )
    current_url = request.build_absolute_uri() # записываем в переменную текущую ссылку
    code = current_url[-18:] # получаем код из ссылки
    report = vk_utility.auth(code)  # функция vk_utility.auth на входе получает код. при помощи кода получает доступ к списку друзей пользователя
                                    # и возвращает список из 5 друзей пользователя
    if 'testcookie' not in request.COOKIES: # проверяем бразуер пользователя на наличие куки из данного приложения
        response = HttpResponse(report)
        response.set_cookie('testcookie', 'VK_auth', max_age=60*60) # если кнопкуи не обнаружено - записываем куки в браузер
    else:
        response = HttpResponse(report)
    return response