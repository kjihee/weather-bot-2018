from sqlalchemy import Column, String, Integer, Boolean, Date, Table, ForeignKey

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ime_db:imedb2018@db-bot.cclpjndcl6jl.ap-northeast-2.rds.amazonaws.com:3306/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Msg(db.Model):
	__tablename__ = 'msg'
	
	id = db.Column(db.Integer, primary_key = True)
	message = db.Column(db.String(255), unique = False)
	pub_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

	def __init__(self, message):
		self.message = message
	def __repr__(self):
		return '<Msg %r>' %self.message

class Location(db.Model):
	__tablename__ = 'location_info'
	
	location_code = db.Column(db.Integer,primary_key = True)
	location_name = db.Column(db.String(45))

	def __init__(self, location_code, location_name):
		self.location_code = location_code
		self.location_name = location_name
	def __repr__(self):
		return '<Location %r >' %self.location_name

class Weather(db.Model):
    __tablename__ = 'weather_info'

    weather_index = Column(Integer,primary_key =True, autoincrement=True)
    selected_date_weather = db.Column(db.Date)
    precipitation_probability = db.Column(db.String(20))
    lowest_temperature = db.Column(db.String(20))
    highest_temperature = db.Column(db.String(20))
    location_code = db.Column(db.Integer, ForeignKey('location_info.location_code'))

    def __init__(self, selected_date_weather, precipitation_probability, lowest_temperature, highest_temperature, location_code):
        self.selected_date_weather = selected_date_weather
        self.precipitation_probability = precipitation_probability
        self.lowest_temperature = lowest_temperature
        self.highest_temperature = highest_temperature
        self.location_code = location_code
   
    def __repr__(self):
        return '<Weather %r>' %self.preipitation_probability


class FineDust(db.Model):
    __tablename__ = 'fine_dust_info'
    
    finedust_index = db.Column(db.Integer,primary_key =True,autoincrement=True) 
    selected_date_fine_dust = db.Column(db.Date)
    fine_dust_concentration = db.Column(db.String(10))
    location_code = db.Column(db.Integer, ForeignKey('location_info.location_code'))

    def __init__(self, selected_date_fine_dust, fine_dust_concentration, location_code):
        self.selected_date_fine_dust = selected_date_fine_dust
        self.fine_dust_concentration = fine_dust_concentration
        self.location_code = location_code

    def __repr__(self):
        return '<FineDust %r>' %self.fine_dust_concentration


class Festival(db.Model):
    __tablename__ = 'festival_info'

    festival_name = db.Column(db.String(100), primary_key=True)
    festival_start_date = db.Column(db.Date)
    festival_end_date = db.Column(db.Date)
    location_code = db.Column(db.Integer, ForeignKey('location_info.location_code'))
    location_detail = db.Column(db.String(45))

    def __init__(self, festival_name, festival_start_date, festival_end_date ,location_code, location_detail):
        self.festival_name = festival_name
        self.festival_start_date = festival_start_date
        self.festival_end_date = festival_end_date
        self.location_code = location_code
        self.location_detail = location_detail
    def __repr__(self):
        return '<Festival %r>' %self.festival_start_date
