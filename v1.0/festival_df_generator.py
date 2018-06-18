from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pandas import DataFrame, Series
import time
import re
import datetime


def generate_festival_df(filepath = 'Festival_df.csv'):
    festival_categories = ['여름꽃축제','바다축제','여름먹거리축제','문화예술축제',
                     '봄축제','벚꽃축제','전통문화축제','봄먹거리축제',
                    '가을축제','단풍축제','대하전어축제','가을먹거리축제',
                    '겨울축제','눈꽃축제','얼음낚시축제','얼음낚시축제']
    driver = webdriver.Chrome('home/ubuntu/weather-bot-2018/chromedriver')


    #data 담을 container 선언
    raw_data_list = []

    #festival_list_count
    for categorie_order in range(len(festival_categories)):
        input_link = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&query=" +festival_categories[categorie_order]
#         print("#'%d'번 카테고리 '%s'" %(categorie_order,input_link))
        driver.get(input_link)
        #링크 접속 후 대기시간
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #page_count
        try:
            page_number = soup.select("#_cs_seasonal_festival > div.ftv_lst > div.pg > span")
            page_number = page_number[0].text.split("/")[1]
        except Exception as e:
#             print("#초기 'page_number' 로딩 시 에러발생. \n 에러내용:", e)
            page_number = '1'
#         print("#현재 페이지는 '%s' 전 페이지 수는 '%s장' 입니다."  %(festival_categories[categorie_order],page_number))
#         print("\n")

        for page in range(int(page_number)):
#             print("#현재 동일페이지에서 '%s'번 시도중입니다."  %(page+1))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices = soup.select(" #_cs_seasonal_festival > div.ftv_lst > ul ")
            notices = notices[0].text.strip().split("  ")
            for number,n in enumerate(notices):
                if n != '':
#                     print(number,n.strip())
                    raw_data_list.append(n.strip())
            if page_number != '1':
                try:
                    driver.find_element_by_xpath("""//*[@id="_cs_seasonal_festival"]/div[3]/div[2]/a[2]""").click()
                except Exception as e:
#                     print("#'다음 목록'버튼 클릭 시 에러발생. \n 에러내용:", e)
                    break
            #링크 접속 후 대기시간
            time.sleep(5)
#         print("\n")

#     print("\n")
#     print("\n")
#     print("수고하셨습니다. 크롤링 작업이 끝났습니다.")




    for number,i in enumerate(raw_data_list):
    #     print(i.strip().split(" "))
        if (number % 2) == 0:
            before_splited = re.findall("([\s\S]+?)(\d{4}.\d{2}.\d{2}~\d{4}.\d{2}.\d{2})",i)
            try:
                name, date= before_splited[0]
                before_dataframe[0].append(name)
                before_dataframe[1].append(datetime.datetime.strptime(date.split('~')[0],'%Y.%m.%d').date())
                before_dataframe[2].append(datetime.datetime.strptime(date.split('~')[1],'%Y.%m.%d').date())
            except IndexError as e:
                before_dataframe[0].append(name)
                before_dataframe[1].append(date.split('~')[0])
                before_dataframe[2].append(None)


        else:
            before_dataframe[3].append(i.strip().split(" ")[0])
            before_dataframe[4].append(i.strip().split(" ")[1])

    Festival_df = DataFrame(list(zip(*before_dataframe)),columns = ["name", "startdate", "enddate", "location_01","location_02"])
    Festival_df.to_csv(filepath,index = False)
