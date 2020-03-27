from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from . import func

def index(request):
    if 'testcookie' not in request.COOKIES: # проверяем браузер пользователя на наличие куки от нашего приложения
        # если куки не обнаружено, значит пользователь зашел к нам в первый раз. Выводим кнопку авторизации
        return render(request, 'auth_app/homePage.html')
    else:
        # если куки обнаружено - перенаправляем пользователя на страницу с выведенными друзьями
        return redirect("https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=https://myvkauth.herokuapp.com/auth_app/friends/&display=page&scope=friends,offline&response_type=code")
     
def friends(request):
    try:
        current_url = request.build_absolute_uri() # записываем в переменную текущую ссылку
        code = current_url[-18:] # срезаем код
        report = func.auth(code)  # функция func.auth на входе получает код. Получает доступ к списку друзей пользователя и возвращает список из 5 случайных друзей пользователя
        if 'testcookie' not in request.COOKIES: # проверяем браузер пользователя на наличие куки от нашего приложения
            response = HttpResponse(report)
            response.set_cookie('testcookie', 'test', max_age=60*60*24*30) # если куки не обнаружены - записываем их в браузер на месяц
        else:
            response = HttpResponse(report)
        return response
    except Exception as e:
        return redirect("https://oauth.vk.com/authorize?client_id=7374940&redirect_uri=https://myvkauth.herokuapp.com/auth_app/friends/&display=page&scope=friends,offline&response_type=code") 