import pymysql
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import datetime
from models import *
import os
from flask import Flask, request, jsonify
from models import FineDust 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ime_db:imedb2018@db-bot.cclpjndcl6jl.ap-northeast-2.rds.amazonaws.com/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


 
location_list = [[1,'강원'],[2,'경기'],[3, '경남'],[4, '경북'],[5, '광주'],[6, '대구'],[7, '대전'],[8, '부산'],[9, '서울'],[10, '세종특별자치시'],[11, '울산'],[12, '인천'],[13, '전남'],[14,'전북'],[15, '제주'],[16, '충남'],[17, '충북'],[18,'값없음']]
location_dict = dict(location_list)
for i in location_list:
    temp = i[0]
    i[0] = i[1]
    i[1] = temp

reverse_location_dict = dict(location_list)


 
@app.route('/keyboard')
def Keyboard():
 
    dataSend = { 
        "type" : "buttons",
        "buttons" : [ "도움말","날씨 조회","미세먼지 조회","축제 조회","축제 추천","옷차림 추천"]
    }
 
    return jsonify(dataSend)

@app.route('/message',methods=['POST','GET'])
def Message():

    dataReceive = request.get_json()
    content = dataReceive['content']
#   user_key = dataReceive['user_key']
 #   user = User_query_filter_by(username=user_key).first()

    msg = Msg(message = content)
    db.session.add(msg)
    db.session.commit()
    print(dataReceive)
    
    #button
    default_button = ["도움말","날씨 조회","미세먼지 조회","축제 조회","축제 추천","옷차림 추천"]
    location_button = ["강원", "경기", "경남", "경북", "광주", "대구", "부산", "서울", "세종특별자치시", "울산", "인천", "전남", "전북", "제주", "충남", "충북"]
    dataSend = {
        "message": {
            "text": "1.도움말, 2.날씨 조회, 3.미세먼지 조회, 4.축제 조회, 5.축제 추천, 6.옷차림 추천"
        }
    }
    
    #1.도움말
    if content == u"도움말":
        dataSend = {
            "message": {
                "text": "날씨와 미세먼지정보, 그에 따른 야외활동과 옷차림을 추천해주는 봇입니다."
            }
        }
    #2.날씨 조회
    elif content == u"날씨 조회" in content :
        dataSend = {
            "message": {
                "text": "입력하신 (날짜)에 따른, 날씨정보를 제공합니다.\n '@1,2018-01-06'형태로 날짜를 입력해주세요. "
            },  
        }
    elif u"@1" in content:
        functional_value,date_value = content.split(",")
        Y,M,D = date_value.split("-")
        input_date_value = date(int(Y),int(M),int(D))
        test_value = Weather.query.filter_by(selected_date_weather = input_date_value).all()
        print_line = "\n# 날짜 조회기능 \n|------날짜------|최저기온|최고기온|지역|\n"
        for i in test_value:
            Day = i.selected_date_weather.strftime('%Y-%m-%d')
            Low = str(i.lowest_temperature)
            High = str(i.highest_temperature)
            Loca = i.location_code
            Sum_of_letter = "|"+Day +"|     "+ Low +"     |     "+ High +"     |"+ location_dict[Loca] + "\n"
            print_line =  print_line + Sum_of_letter
        print (len(print_line))
        if len(print_line) < 50:
            print_line = print_line +  "\n검색할 정보가 없습니다."        
        dataSend = {
            "message": {
                "text": "날씨조회 기능 실시합니다. \n"+print_line
            }
        }

    #3.미세먼지 조회
    elif content ==u"미세먼지 조회" in content:
        dataSend ={
            "message": {
                 "text" :"입력하신 (날짜|지역)에 해당하는, 미세먼지 정보를 제공합니다.\n '@2,2018-01-06,부산'형태로 날짜를 입력해주세요. "
          }
        }
    elif u"@2" in content:
        functional_value,date_value,location_value = content.split(",")
        print(content.split(","))
        Y,M,D = date_value.split("-")
        input_location_value = reverse_location_dict[location_value]
        input_date_value = date(int(Y),int(M),int(D))
        test_value = FineDust.query.filter_by(selected_date_fine_dust= input_date_value,location_code = input_location_value).all()
        #tested_value = test_value.filter_by(location_code = 1).all()
        print_line = "\n# 미세먼지 조회기능"
        for i in test_value:
            print(i.location_code)
            Day = i.selected_date_fine_dust.strftime('%Y-%m-%d')
            Finedust = i.fine_dust_concentration
            Loca = i.location_code
            Sum_of_letter = "\n날짜:"+Day +"\n미세먼지 농도:"+ Finedust +"\n지역:"+ location_dict[Loca] + "\n"
            print_line =  print_line + Sum_of_letter
        print (len(print_line))
        if len(print_line) < 30:
            print_line = print_line +  "\n검색할 정보가 없습니다."


        dataSend = {
            "message": {
                "text": "미세먼지조회 기능 실시합니다. \n" + print_line
            }
        }
    #4.축제 조회
    elif content == u"축제 추천" in content:
        dataSend = {
            "message": {
                "text": "입력하신 (날짜|지역)의 축제 및 날짜 정보를 고려하여, 축제를 추천해줍니다.\n '@4,2018-01-06,부산'형태로 날짜를 입력해주세요. "
            }
        }
    elif u"@4" in content:
        
        functional_value,date_value,location_value = content.split(",")
        Y,M,D = date_value.split("-")
        input_location_value = reverse_location_dict[location_value]
        input_date_value = date(int(Y),int(M),int(D))
        test_value = Festival.query.filter_by(location_code = input_location_value).all()
        print_line = "\n# 축체추천 기능"
        for i in test_value:
            print(i)
            if (input_date_value >= i.festival_start_date ) and (input_date_value <= i.festival_end_date):
                print("넘어왔습니다.")
                finedust_opp = FineDust.query.filter_by(selected_date_fine_dust= input_date_value,location_code = input_location_value).first()
                weather_opp = Weather.query.filter_by(selected_date_weather =  input_date_value, location_code = input_location_value).first()
                print(type(finedust_opp),type(weather_opp))
                Name = i.festival_name
                start_Day = i.festival_start_date.strftime('%Y-%m-%d')
                end_Day = i.festival_end_date.strftime('%Y-%m-%d')
                ddate = input_date_value.strftime('%Y-%m-%d')
                Loca = i.location_code
                Delo = i.location_detail
                finedust = finedust_opp.fine_dust_concentration
                #finedust,weather_down,weather_up = ['1','2','3']
                weather_down = weather_opp.lowest_temperature
                weather_up = weather_opp.highest_temperature
                temp = str(round((int(weather_down)+int(weather_up))/2))
                Sum_of_letter = "\n축제명:"+Name + "\n검색일:"+ ddate +"\n평균기온:"+ temp+"\n미세먼지농도:"+finedust +"\n지역:"+ location_dict[Loca] +", "+Delo + "\n"
                print_line =  print_line + Sum_of_letter
        print (len(print_line))
        if len(print_line) < 30:
            print_line = print_line +  "\n검색할 정보가 없습니다."





        dataSend = {
        "message": {
            "text": "축제추천 기능 실시합니다.\n" + print_line
        }
        }
    #5.축제 추천
    elif content == u"축제 조회" in content:
        dataSend = {
            "message": {
                "text": "입력하신 (날짜|지역)의 축제 및 날짜 정보를 출력해줍니다..\n '@3,2018-01-06,부산'형태로 날짜를 입력해주세요. "

                


            }
        }
    elif u"@3" in content:
        functional_value,date_value,location_value = content.split(",")
        print(content.split(","))
        Y,M,D = date_value.split("-")
        input_location_value = reverse_location_dict[location_value]
        input_date_value = date(int(Y),int(M),int(D))
        test_value = Festival.query.filter_by(location_code = input_location_value).all()
        print_line = "\n# 축제 조회기능"
        print(len(test_value))
        print(type(test_value),test_value)
        for i in test_value:
            if (input_date_value >=  i.festival_start_date ) and (input_date_value <=  i.festival_end_date):
                print(i.location_code)
                Name = i.festival_name
                start_Day = i.festival_start_date.strftime('%Y-%m-%d')
                end_Day = i.festival_end_date.strftime('%Y-%m-%d')
                Loca = i.location_code
                Delo = i.location_detail
                Sum_of_letter = "\n축제명:"+Name + "\n축제기간:"+start_Day +" ~ "+ end_Day +"\n지역:"+ location_dict[Loca] +", "+Delo+ "\n"
                print_line =  print_line + Sum_of_letter

        print (len(print_line))
        if len(print_line) < 30:
            print_line = print_line +  "\n검색할 정보가 없습니다."


        dataSend = {
        "message": {
            "text": "축제조회 기능 실시합니다.\n"+print_line
        }
        }
    #6.옷차림 추천
    elif content == u"옷차림 추천"  in content:
        dataSend = {
            "message": {
                "text": " 입력하신 (날짜|지역)의 평균 기온을 고려하여, 옷차림을 추천해줍니다. \n '@5,2018-01-06,부산'형태로 날짜를 입력해주세요. "
            }
        }
    elif u"@5" in content:
        functional_value,date_value,location_value = content.split(",")
        input_location_value = reverse_location_dict[location_value]
        Y,M,D = date_value.split("-")
        input_date_value = date(int(Y),int(M),int(D))
        test_value = Weather.query.filter_by(selected_date_weather = input_date_value, location_code = input_location_value).all()
        print_line = "\n# 옷차림 추천기능\n"
        for i in test_value:
            Day = i.selected_date_weather.strftime('%Y-%m-%d')
            Low = str(i.lowest_temperature)
            High = str(i.highest_temperature)
            Loca = i.location_code
            Sum_of_letter = "날짜:"+Day +"\n최저기온:"+ Low +"\n최고기온:"+ High +"\n지역:"+ location_dict[Loca] + "\n\n 추천>>"
            print_line =  print_line + Sum_of_letter
        
            average_temperature = round( (int(High)+ int(Low))/2)

            if average_temperature >=28 :
                print_line = print_line + "민소매/반팔 + 반바지/치마를 추천합니다"
            elif average_temperature >= 24 and average_temperature<28 :
                print_line = print_line + "반팔/얇은 긴팔 + 반바지를 추천합니다"
            elif average_temperature >=20 and average_temperature<24 :
                print_line = print_line + "얇은 니트/가디건/긴팔티/후드티 + 면바지/슬랙스를 추천합니다"
            elif average_temperature >=17 and average_temperature<20 :
                print_line = print_line + "니트/가디건/맨투맨/ + 청바지/면바지/슬랙스/원피스를 추천합니다"
            elif average_temperature >= 11 and average_temperature<17:
                print_line = print_line + "자켓/셔츠/가디건/간절기 야상(안에 두꺼운 옷)을 추천합니다"
            elif average_temperature >= 6 and average_temperature<11:
                print_line = print_line + "코트/간절기 야상을 추천합니다"
            elif average_temperature >= 0 and average_temperature<6 :
                print_line = print_line + "코트/가죽자켓/패딩을 추천합니다"
            else:
                print_line = print_line + "두꺼운 코트/패딩/퍼를 추천합니다"
        print (len(print_line))
        if len(print_line) < 50:
            print_line = print_line +  "\n검색할 정보가 없습니다."



        dataSend = {
        "message": {
            "text": "옷차림 추천 기능 실시합니다. \n" + print_line
        }
        }
    else:
        dataSend = {
            "message": {
                "text": "응답할 수 없는 답변입니다."
            }
        }


    return jsonify(dataSend)
 
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
