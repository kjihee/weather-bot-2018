from datetime import date
from models import *
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import datetime
festival_df=pd.read_csv("./new_Festival_df.csv") 
#festival_df['startdate'] = pd.to_datetime(festival_df["startdate"],infer_datetime_format=True)
#festival_df['enddate'] = pd.to_datetime(festival_df['enddate'],infer_datetime_format=True)

location_list = [[1,'강원'],[2,'경기'],[3, '경남'],[4, '경북'],[5, '광주'],[6, '대구'],[7, '대전'],[8, '부산'],
[9, '서울'],[10, '세종특별자치시'],[11, '울산'],[12, '인천'],[13, '전남'],[14,'전북'],[15, '제주'],[16, '충남'],[17, '충북'],[18,'값없음']]

for i in location_list:
    temp = i[0]
    i[0] = i[1]
    i[1] = temp
festival_df.fillna(0)
location_dict = dict(location_list)
print("festival data를 입력합니다.")
for Iist in festival_df.values.tolist():
    print(Iist)
    garbage,name,startdate, enddate, location_01, location_02 = Iist
    if "." in startdate:
        Y,M,D = startdate.split(".")
        start_date = date(int(Y),int(M),int(D))
    elif startdate == '':
        start_date = None
    else:
        Y,M,D = startdate.split("-")
        start_date = date(int(Y),int(M),int(D))
    print(start_date)
    if "." in str(enddate):
        Y,M,D = enddate.split(".")
        end_date = date(int(Y),int(M),int(D))
    elif enddate == '':
        end_date = None
    elif str(enddate) == 'nan':
        end_date = None
    else:
        Y,M,D = enddate.split("-")
        end_date = date(int(Y),int(M),int(D))
    print(end_date)
    insert_value = Festival(festival_name = name, festival_start_date  = start_date, festival_end_date = end_date, location_code= int(location_dict[location_01]), location_detail = location_02)
    db.session.add(insert_value)
db.session.commit()
db.session.close()

print("Data삽입이  완료되었습니다.")
