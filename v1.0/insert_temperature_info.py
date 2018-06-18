
from models import Weather, db
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from datetime import date
import datetime



# 엑셀 불러오기
temperature_sett  = pd.read_excel('./weather-bot-2018/temperature.xlsx')




# 지역 사전 생성
location_list = [[1,'강원'],[2,'경기'],[3, '경남'],[4, '경북'],[5, '광주'],[6, '대구'],[7, '대전'],[8, '부산'],[9,'서울'],[10, '세종특별자치시'],[11,'울산'],[12,'인천'],[13,'전남'],[14,'전북'],[15, '제주'],[16,'충남'],[17,'충북'],[18,'값없음']]

for i in location_list:
	temp = i[0]
	i[0] = i[1]
	i[1] = temp

location_dict = dict(location_list)


# 컬럼 리스트 생성
columns_name = temperature_sett.keys()


# 인설트 "nested for loop"
for count,i in enumerate(columns_name):
	if count != 0:
		for ccount, record in enumerate(temperature_sett[i]):
                     
			
			# 날짜 벨류 생성
			Y,M,D = i.split("-")
			date_value = date(int(Y),int(M),int(D))
               

			#온도, 강수량 분할
			P,L,H=record.split("/")
			low_temperature =  int(L.strip())
			high_temperature = int(H.strip())
			pre_probability = P
			insert_value = Weather(selected_date_weather=date_value,precipitation_probability=pre_probability, lowest_temperature=low_temperature,highest_temperature=high_temperature , location_code  = location_dict[temperature_sett['지역'][ccount]])
			db.session.add(insert_value)

# 마지막 commit
db.session.commit()

