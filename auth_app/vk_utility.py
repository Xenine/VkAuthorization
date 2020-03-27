import json
import urllib
import urllib.request
import requests
import time

def auth(code):
    """Функция получает значения code для получения ключа доступа. Затем при помощи
    значения code сервер приложения получает ключ доступа access_token для доступа к API ВКонтакте.
    Далее при помощи API ВКонтакте получает имя авторизованного пользователя и список из 5 его друзей,
    выбранных в произвольном порядке. Функция возвращает сообщение с именем авторизованного
    пользователя и списком из 5 его друзей"""
    request_link = 'https://oauth.vk.com/access_token?client_id=7374940&client_secret=l6n54t5ztiKcZcVDI6xF&redirect_uri=https://myvkauth.herokuapp.com/auth_app/friends/&code={0}'
    request_link = request_link.format(code)
    r = requests.get(url=request_link) # через API запрос получаем словарь в формате JSON
    data = r.json()
    print(data)
    access_token = data['access_token'] #  получаем access token
    user_id = data['user_id'] #  получаем ID авторизованного пользователя
    request_link = "https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&access_token={1}&v=5.103"
    request_link = request_link.format(user_id, access_token)
    r = requests.get(url=request_link) # через API запрос получаем словарь в формате JSON
    data = r.json()
    first_name = data['response'][0]['first_name'] # получаем имя авторизованного пользователя
    last_name = data['response'][0]['last_name'] # получаем фамилию авторизованного пользователя
    greeting_string = '<p style="font-size:28px;">Здравствуйте, {0} {1}, вы авторизованы.</p><br>'
    greeting_string = greeting_string.format(first_name, last_name)
    request_link = "https://api.vk.com/method/friends.get?user_ids={0}&order=random&count=5&fields=domain&access_token={1}&v=5.103 "  # создаем запрос на 5 друзей, выбранных в случайном порядке
    request_link = request_link.format(user_id, access_token)
    r = requests.get(url=request_link) # через API запрос получаем словарь в формате JSON
    data = r.json()
    array_of_friends_ID = data['response']['items'] # получаем массив словарей имен, фамилий и id друзей 
    greeting_string += '<p style="font-size:28px;">5 друзей из вашего контакт листа, выбранных в случайном порядке:</p><br>'
    for i in range(5): 
        temp_first_name = array_of_friends_ID[i]['first_name']
        temp_last_name = array_of_friends_ID[i]['last_name']
        temp_id = array_of_friends_ID[i]['id']
        temp_new_string = '{0} {1} \n'
        temp_new_string = temp_new_string.format(temp_first_name, temp_last_name)
        new_string = '<a href="https://vk.com/id{0}" style="font-size:20px;">{1}</a><br>'
        new_string = new_string.format(temp_id, temp_new_string)
        greeting_string += new_string

    return greeting_string