from django.shortcuts import render
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys #Keys=웹 통해 값 입력할 때 사용하는 라이브러리(키보드)
from selenium.webdriver.common.by import By
import pandas as pd
import time #time= 컴퓨터에게 쉬는시간 부여하는 라이브러리
import urllib # 한글주소로 변환
from django.http import JsonResponse

# Create your views here.



def crawling(request,keyword):
### for Windows 
    # chromedriver 위치에서 코드작업 필수
    # 한글은 주소에서 %문자로 인코딩되므로 파이썬 라이브러리로 인코드해준다

    encoded_keyword = urllib.parse.quote(keyword)


    #웹사이트 열기
    driver = webdriver.Chrome() #webdriver야, chrome 실행시켜라. 경로는 ()에 있어. 크롤링 작업공간과 크롬 드라이버 같은 공간에 있을 경우 공란 ().
    driver.get("https://search.shopping.naver.com/search/all?query="+encoded_keyword+"&cat_id=&frm=NVSHATC") #네이버 페이지로 이동
    driver.implicitly_wait(4) #로딩 끝날 때까지 10초 기다리기



    # 상품정보 div찾음

    item_selector = "#content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div > div > div > div.adProduct_info_area__dTSZf > div.adProduct_title__amInq > a"
    price_selector = "#content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div > div > div > div.adProduct_info_area__dTSZf > div.adProduct_price_area__yA7Ad > strong > span.price > span > em"
    #content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(1) > div
    items = driver.find_elements(By.CSS_SELECTOR, item_selector)
    prices = driver.find_elements(By.CSS_SELECTOR, price_selector)

    message_list=["네이버쇼핑몰에서 검색한 내용입니다."]
    for item, price in zip(items, prices):
        message_list.append(item.text+"\n"+price.text)

    message = '\n'.join(message_list)

    return message


