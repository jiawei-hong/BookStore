from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect


from bs4 import BeautifulSoup
import urllib.request as req
import requests
import json
import os
import time


# Create your views here.

def hot_book_img(book_ID_url):
    book_url = f'https://tclwebdata.s3.amazonaws.com/EBSRepos/EBSRepos/Images/cover450/{book_ID_url}.png'
    return book_url

def hot_book_total_url(book_ID):
    book_content = f'https://m.ebookservice.tw/api/3.00/ks/BookProfile/{book_ID}'
    return book_content

def read_hotbook_total_url(url):
    book_con =req.Request(url,headers={
        'cookie':'mid=WLsL4gAEAAGl0Wjoc8Dv6CH_iYnP; mcd=3; ds_user_id=1926542376; csrftoken=9aasLCq0vb2dUQWY9j1rjP11aejod1wS; sessionid=1926542376%3AG5zq9okSZhBxWx%3A8; ig_did=8675D711-4D34-4DBA-8751-F9E4E3B8FA63; shbid=17721; shbts=1602880097.7694821; rur=VLL; urlgen="{\"61.228.154.31\": 3462}:1kTWVn:7qfV2Cxf3rs1oZ9BUi45bNQ18T4',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        })
    with req.urlopen(book_con) as response:
        data = response.read().decode('utf8')
    books = json.loads(data)
    return books

def hot_book(request, date_time=time.strftime(f'%Y/%m/%d', time.localtime()), book_number=1):
    try:
        try:
            book_number = request.GET['book_searcg']
        except:
            pass
        if time.strptime(date_time, f"%Y/%m/%d"):
            hot_book_url = f'https://m.ebookservice.tw/api/3.00/kl;taipei;nt;ty;ml;ntc;cy;cyc;tn;ks;pt;ph;il;km;hc;hcc;ylc;ntl2;tt;tcl/TclPopularBook/?beginDate={date_time}&endDate={date_time}%2023:59:59&type=book&takeSize={book_number}'
            # hot_book_url = f'https://m.ebookservice.tw/api/3.00/kl;taipei;nt;ty;ml;ntc;cy;cyc;tn;ks;pt;ph;il;km;hc;hcc;ylc;ntl2;tt;tcl/TclPopularBook/?beginDate=2020/11/5&endDate=2020/11/5%2023:59:59&type=book&takeSize={book_number}'
            requests=req.Request(hot_book_url,headers={
                'cookie':'mid=WLsL4gAEAAGl0Wjoc8Dv6CH_iYnP; mcd=3; ds_user_id=1926542376; csrftoken=9aasLCq0vb2dUQWY9j1rjP11aejod1wS; sessionid=1926542376%3AG5zq9okSZhBxWx%3A8; ig_did=8675D711-4D34-4DBA-8751-F9E4E3B8FA63; shbid=17721; shbts=1602880097.7694821; rur=VLL; urlgen="{\"61.228.154.31\": 3462}:1kTWVn:7qfV2Cxf3rs1oZ9BUi45bNQ18T4',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            })
            with req.urlopen(requests) as response:
                data = response.read().decode('utf8')

            datas = json.loads(data)
            datas =datas['List']
            book_ID_dic = {}
            # book_url_list= []
            
            for date in datas:
                book_flash = {}
                book_ID = date['TinyBook']['BookId']
                book_contents = hot_book_total_url(book_ID)
                book_contents = read_hotbook_total_url(book_contents)

                book_flash.setdefault('book_img_url',hot_book_img(book_ID)) #圖片網址
                book_flash.setdefault('TitleCache',book_contents['TitleCache']) #標題
                book_flash.setdefault('Author',book_contents['Author']) #作者
                book_flash.setdefault('PublisherName',book_contents['PublisherName'])  # 出版社
                book_flash.setdefault('TotalPage',book_contents['TotalPage']) #總頁數
                book_flash.setdefault('UpdateDate',book_contents['UpdateDate']) #上傳時間
                book_flash.setdefault('Description',book_contents['Description']) #描述
                book_flash.setdefault('ISBN',book_contents['ISBN']) # 書本編號
                
                book_ID_dic.setdefault(book_ID,book_flash) # {ID:[img_url,TitleCache標題,Author作者,PublisherName出版社,TotalPage總頁數,UpdateDate上傳時間,Description描述,ISBN書本編號]}
                # book_url_list.append(hot_book_img(book_ID))   'book_url_list':book_url_list #GET圖片網址

            return render(request , 'hot-book.html' ,{ 'date_time':date_time, 'book_number':book_number, 'book_ID_dic':book_ID_dic})
    except:
        return render(request,'hot-book.html',{'date_time':"錯誤"})

def information_book(request, pagesize=24, pageno=1):
    try:
        try:
            if bool(request.GET['bool']) == True:
                pageno = int(request.GET['next_number'])
                pageno += int(request.GET['next'])
        except:
            pass
        try:
            if bool(request.GET['bool-back']) == True:
                pageno = int(request.GET['back_number'])
                pageno -= int(request.GET['back-up'])
        except:
            pass
        try:
            if pageno > int(request.GET['page_total']):
                pageno = int(request.GET['page_total'])
        except:
            pass
        
        informa_book_url = f'https://m.ebookservice.tw/api/3.00/ks/BookList/?pageSize=24&pageNo={pageno}&classification=TCL144&keyword='
        requests = req.Request(informa_book_url,headers={
            'cookie':'mid=WLsL4gAEAAGl0Wjoc8Dv6CH_iYnP; mcd=3; ds_user_id=1926542376; csrftoken=9aasLCq0vb2dUQWY9j1rjP11aejod1wS; sessionid=1926542376%3AG5zq9okSZhBxWx%3A8; ig_did=8675D711-4D34-4DBA-8751-F9E4E3B8FA63; shbid=17721; shbts=1602880097.7694821; rur=VLL; urlgen="{\"61.228.154.31\": 3462}:1kTWVn:7qfV2Cxf3rs1oZ9BUi45bNQ18T4',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        })
        with req.urlopen(requests) as response:
            data = response.read().decode('utf8')
        
        data = json.loads(data)
        page_total = data['TotalRecordCount']
        datas = data['List']

        book_ID_dic = {}
        for date in datas:
            book_flash = {}
            book_ID = date['TinyBook']['BookId']
            book_contents = hot_book_total_url(book_ID)
            book_contents = read_hotbook_total_url(book_contents)

            book_flash.setdefault('book_img_url',hot_book_img(book_ID)) #圖片網址
            book_flash.setdefault('TitleCache',book_contents['TitleCache']) #標題
            book_flash.setdefault('Author',book_contents['Author']) #作者
            book_flash.setdefault('PublisherName',book_contents['PublisherName'])  # 出版社
            book_flash.setdefault('TotalPage',book_contents['TotalPage']) #總頁數
            book_flash.setdefault('UpdateDate',book_contents['UpdateDate']) #上傳時間
            book_flash.setdefault('Description',book_contents['Description']) #描述
            book_flash.setdefault('ISBN',book_contents['ISBN']) # 書本編號
            
            book_ID_dic.setdefault(book_ID,book_flash)
        return render(request , 'information-book.html' ,{'book_ID_dic':book_ID_dic , 'pageno':pageno , 'page_total':page_total})
    except:
        return render(request,'information-book.html',{'date_time':"錯誤"})

