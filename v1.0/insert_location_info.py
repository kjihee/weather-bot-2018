from models import Location, db
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

location_record = [[1,'강원'],[2,'경기'],[3, '경남'],[4, '경북'],[5, '광주'],[6, '대구'],[7, '대전'],[8, '부산'],
[9, '서울'],[10, '세종특별자치시'],[11, '울산'],[12, '인천'],[13, '전남'],[14,'전북'],[15, '제주'],[16, '충남'],[17, '충북'],[18,'값없음']]

# dict 변환
#location_dict =dict(location_record)
#print(location_dict)

location_df = DataFrame(location_record,columns=['code','name'])
print("location data를 입력합니다.")

for i in location_df.values.tolist():
	print(i)

for Iist in location_df.values.tolist():
	code,name = Iist
	print(Iist,code,name)
	insert_value = Location(location_code = code, location_name = name)
	db.session.add(insert_value)
db.session.commit()
print("Data삽입이  완료되었습니다.")

