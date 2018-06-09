from sqlalchemy import Column, String, Integer, Boolean, Date, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:@localhost:3306/weather_bot_2018')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Location(Base):
    __tablename__ = 'location_info'

    location_name = Column(String(20), primary_key=True)

    def __init__(self, location_name):
        self.location_name = location_name


class Weather(Base):
    __tablename__ = 'weather_info'

    selected_date_weather = Column(Date, primary_key=True)
    precipitation_probability = Column((10))
    lowest_temperature = Column(String(10))
    highest_temperature = Column(String(10))
    location_name = Column(String(20), foreignkey=True)

    def __init__(self, selected_date_weather, precipitation_probability, lowest_temperature, highest_temperature, location_name):
        self.selected_date_weather = selected_date_weather
        self.precipitation_probability = precipitation_probability
        self.lowest_temperature = lowest_temperature
        self.highest_temperature = highest_temperature
        self.location_name = location_name


class FineDust(Base):
    __tablename__ = 'fine_dust_info'

    selected_date_fine_dust = Column(Date, primary_key=True)
    fine_dust_concentration = Column(String(10))
    location_name = Column(String(20), foreignkey=True)

    def __init__(self, selected_date_fine_dust, fine_dust_concentration, location_name):
        self.selected_date_fine_dust = selected_date_fine_dust
        self.fine_dust_concentration = fine_dust_concentration
        self.location_name = location_name


class Festival(Base):
    __tablename__ = 'festival_info'

    festival_name = Column(String(100), primary_key=True)
    festival_start_date = Column(Date)
    festival_end_date = Column(Date)
    location_name = Column(String(20), foreignkey=True)
    location_name_detail = Column(String(20))

    def __init(self, festival_name, festival_start_date, festival_end_date location_name, location_name_detail):
        self.festival_name = festival_name
        self.festival_start_date = festival_start_date
        self.festival_end_date = festival_end_date
        self.location_name = location_name
        self.location_name_detail = location_name_detail
