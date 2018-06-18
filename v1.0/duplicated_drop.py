
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pandas import DataFrame, Series
import time
import re
import datetime

from sqlalchemy.orm import sessionmaker
from datetime import date
from sqlalchemy import create_engine,func
import json
import os
import urllib
import pymysql




festival_df=pd.read_csv("./weather-bot-2018/data/Festival_df.csv")

festival1 = festival_df.drop_duplicates(['name'])


festival1.to_csv("./new_Festival_df.csv")
