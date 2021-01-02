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


def keyword(request):
    return render(request, 'tenlong/keyword.html', {
        'navbar': get_navbar(),
        'keyword': request.POST['keyword']
    })


def get_keyword_books(request, book_name, book_page):
    req_text = requests.get(f'https://www.tenlong.com.tw/search', {
        'keyword': book_name,
        'page': book_page
    }).text
    books = []
    book_soup = BeautifulSoup(req_text, 'html.parser').find('div', class_='search-result-list').find('ul').find_all(
        'li', class_=lambda x: x != 'promo')

    for book in book_soup:
        try:
            book_link = book.find('a', class_='cover').get('href')
            book_img = book.find('a', class_='cover').find('img').get('src')
            book_info = '/'.join([x.text for x in book.find('div', class_='book-data').find('ul', class_='item-info').find('li', class_='basic').find_all('span')])
            book_status = '/'.join([x.text.strip() for x in book.find('div', class_='book-data').find('ul', class_='item-info').find('li', class_='pricing').find_all('span')])

            books.append({
                'link': f'https://www.tenlong.com.tw/{book_link}',
                'img': book_img,
                'info': book_info,
                'status': book_status
            })
        except:
            pass

    return HttpResponse(json.dumps(books))


def publisher(request, publisher_id):
    return render(request, 'tenlong/books.html', {
        'navbar': get_navbar(),
        'publishers_id': publisher_id
    })


def publishers(request):
    req_text = requests.get('https://www.tenlong.com.tw//publishers').text
    publisher_soup = BeautifulSoup(req_text, 'html.parser').find('ul', class_='category-list--full').findAll('a')
    publisher_data = [{
        'name': item.text,
        'link': item.get('href')
    } for item in publisher_soup]

    return render(request, 'tenlong/publishers.html', {
        'navbar': get_navbar(),
        'publishers': publisher_data
    })


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


def get_books(request, book_species, book_id, book_page):
    req_text = requests.get(f'https://www.tenlong.com.tw/{book_species}/{book_id}', {
        'page': book_page
    }).text
    book_soup = BeautifulSoup(req_text, 'html.parser').find('div', class_='list-wrapper').find('ul').findAll('li',
                                                                                                             class_='single-book')
    book_data = []

    for book_ele in book_soup:
        book_title = book_ele.find('strong', class_='title')
        book_price = list(
            filter(lambda x: x != '', book_ele.find('div', class_='pricing').text.strip().split(' ')))
        book_data.append({
            'name': book_title.find('a').text,
            'img_link': book_ele.find('a', class_='cover').find('img').get('src'),
            'price': book_price[1 if len(book_price) > 1 else 0],
            'link': 'https://www.tenlong.com.tw' + book_title.find('a').get('href')
        })

    return HttpResponse(json.dumps(book_data))
