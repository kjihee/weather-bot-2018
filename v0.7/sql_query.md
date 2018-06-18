## 기능 query문 


### 날씨조회
1. SELECT loc.location_name ,round(avg(lowest_temperature+highest_temperature)/2) as average, min(lowest_temperature) as minimum, max(highest_temperature) as maximum 
FROM test_db.weather_info as wea 
inner join test_db.location_info as loc 
on wea.location_code=loc.location_code
group by loc.location_name;

### 미세먼지 조회
2. SELECT loc.location_name as location_name, selected_date_fine_dust as selected_date, fine_dust_concentration
FROM test_db.fine_dust_info as dusts 
inner join test_db.location_info as loc on dusts.location_code=loc.location_code
where fine_dust_concentration like "%쁨" and selected_date_fine_dust='2018-06-15';

### 축제정보 조회
3. SELECT loc.location_name, fes.location_detail, fes.festival_name, fes.festival_start_date, fes.festival_end_date
FROM test_db.festival_info as fes
INNER JOIN test_db.location_info as loc
ON fes.location_code = loc.location_code
where  fes.festival_start_date <='2017-08-10'
and fes.festival_end_date >= '2017-08-10';

### 축제 추천
4. select loc.location_name, fes.location_detail, fes.festival_name, fes.festival_start_date, fes.festival_end_date
FROM test_db.festival_info as fes
INNER JOIN test_db.location_info as loc
ON fes.location_code = loc.location_code
inner join test_db.fine_dust_info as fine
on fine.location_code = fes.location_code
inner join test_db.weather_info as wea
on wea.location_code = fes.location_code
where  fes.festival_start_date <='2017-08-10'
and fes.festival_end_date >= '2017-08-10' 
and fine.fine_dust_concentration not like "%나쁨" 
and wea.precipitation_probability != "비옴" and loc.location_name = "강원"  
group by location_detail;

