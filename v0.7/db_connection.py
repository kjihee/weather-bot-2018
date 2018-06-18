from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pymysql
import json
from sqlalchemy.ext.declarative import declarative_base

def connection_config():
    with open("config.json","r",encoding="utf8") as f:
        contents = f.read()
        json_data = json.loads(contents.encode("utf-8"))

    host =json_data["mydb"][0]["host"]
    db_id =json_data["mydb"][1]["db_id"]
    db_password =json_data["mydb"][2]["db_password"]
    db_name =json_data["mydb"][3]["db_name"]
    port = json_data["mydb"][4]["port"]

    return host, db_id, db_password, db_name, port

def config_engine():
    host, db_id, db_password, db_name, port= connection_config()
#     engine = create_engine('mysql+pymysql://root:1234@localhost:3306/korean_stock?charset=utf8')
    engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(db_id ,db_password, host, port,db_name))
    return engine

def make_session():
    engine = config_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def make_cursor():
    
    host, db_id, db_password, db_name, port= connection_config()
#     engine = create_engine('mysql+pymysql://root:1234@localhost:3306/korean_stock?charset=utf8')
   
    session = make_session()
    conn = pymysql.connect(host=host, user= db_id, password=str(db_password),  charset='utf8')
    curs = conn.cursor()
    curs.execute('USE %s' %db_name)
    return curs


