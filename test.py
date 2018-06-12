

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask import Flask, request, jsonify
 
  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ime_db:imedb2018@db-bot.cclpjndcl6jl.ap-northeast-2.rds.amazonaws.com/test_db'
db = SQLAlchemy(app)
 
app = Flask(__name__)


 
