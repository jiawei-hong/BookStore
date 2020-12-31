from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import json


# Create your views here.

def index(request):
    return render(request, 'tenlong/index.html', {
        'navbar': get_navbar(),
    })


def special(request, special_id):
    return render(request, 'tenlong/books.html', {
        'navbar': get_navbar(),
        'special_id': special_id
    })


def publisher(request, publisher_id):
    return render(request, 'tenlong/publisher_view.html', {
        'navbar': get_navbar(),
        'publisher_id': publisher_id
    })


def get_keyword(request):
    return HttpResponse(request.POST['keyword'])


def get_navbar():
    req_text = requests.get('https://www.tenlong.com.tw/').text
    sidebar_data = []
    sidebars = BeautifulSoup(req_text, 'html.parser').findAll('div', class_='sidebox')

    for sidebar in sidebars:
        sidebar_text = sidebar.find('h2').text
        sidebar_not_hidden = ['特價書籍']

        if sidebar_text in sidebar_not_hidden:
            sidebar_data.append({
                'name': sidebar.find('h2').text,
                'link_dict': [{
                    'link': str(link.find('a').get('href')),
                    'text': link.find('a').text
                } for link in sidebar.find('ul').find_all('li')]
            })

    return sidebar_data


def get_special_books(request, special_id, page):
    req_text = requests.get(f'https://www.tenlong.com.tw/special/{special_id}', {
        'page': page
    }).text
    special_soup = BeautifulSoup(req_text, 'html.parser').find('div', class_='list-wrapper').find('ul').findAll('li',
                                                                                                                class_='single-book')
    special_data = []

    for special_ele in special_soup:
        special_title = special_ele.find('strong', class_='title')
        special_price = list(
            filter(lambda x: x != '', special_ele.find('div', class_='pricing').text.replace('\n', '').split(' ')))
        special_data.append({
            'name': special_title.find('a').text,
            'img_link': special_ele.find('a', class_='cover').find('img').get('src'),
            'price': special_price[1 if len(special_price) > 1 else 0],
            'link': 'https://www.tenlong.com.tw' + special_title.find('a').get('href')
        })

    return HttpResponse(json.dumps(special_data))


def get_publisher(request):
    req_text = requests.get('https://www.tenlong.com.tw//publishers').text
    publisher_data = []
    publisher_soup = BeautifulSoup(req_text, 'html.parser').find('ul', class_='category-list--full').findAll('a')

    for publisher in publisher_soup:
        publisher_data.append({
            'name': publisher.text,
            'link': publisher.get('href')
        })

    return render(request, 'tenlong/publishers.html', {
        'navbar': get_navbar(),
        'publishers': publisher_data
    })


def get_publisher_books(request, publisher_id, page):
    req_text = requests.get(f'https://www.tenlong.com.tw/publishers/{publisher_id}', {
        'page': page
    }).text
    publisher_soup = BeautifulSoup(req_text, 'html.parser').find('div', class_='list-wrapper').find('ul').findAll('li',
                                                                                                                  class_='single-book')
    publisher_data = []

    for publisher_ele in publisher_soup:
        publisher_title = publisher_ele.find('strong', class_='title')
        publisher_price = list(
            filter(lambda x: x != '', publisher_ele.find('div', class_='pricing').text.replace('\n', '').split(' ')))
        publisher_data.append({
            'name': publisher_title.find('a').text,
            'img_link': publisher_ele.find('a', class_='cover').find('img').get('src'),
            'price': publisher_price[1 if len(publisher_price) > 1 else 0],
            'link': 'https://www.tenlong.com.tw' + publisher_title.find('a').get('href')
        })

    return HttpResponse(json.dumps(publisher_data))
