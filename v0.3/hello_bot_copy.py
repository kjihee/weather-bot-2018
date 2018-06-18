
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from flask import Flask, request, jsonify
 
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ime_db:imedb2018@db-bot.cclpjndcl6jl.ap-northeast-2.rds.amazonaws.com/test_db'
db = SQLAlchemy(app)
 
app = Flask(__name__)
 
 
 
@app.route('/keyboard')
def Keyboard():
 
    dataSend = {
        "type" : "buttons",
        "buttons" : [ "도움말","날씨 조회","미세먼지 조회","축제 추천","옷차림 추천"]
    }
 
    return jsonify(dataSend)
 
 
 
@app.route('/message', methods=['POST'])
def Message():
    
    dataReceive = request.get_json()
    content = dataReceive['content']
    user_key = dataReceive['user_key']
    user = User_query_filter_by(username=user_key).first()
    print(user)	
    
    if user is None:
        import random
        rand_number = int(random.random()?*1000000)
        new_user = User(username = user_key, email='{}@example.com'.format(rand_number))
        db.session.add(new_user)
        db.session.commit()

    user = User.query.filter_by(username = user_key).first()
    msg = Msg(message = content , user_id = user.id)
    db.session.commit()

    if content == u"도움말":
        dataSend = {
            "message": {
                "text": "날씨와 미세먼지정보, 그에 따른 야외활동과 옷차림을 추천해주는 봇입니다."
            }
        }
    elif content == u"날씨 조회":
        dataSend = {
            "message": {
                "text": "날씨정보를 제공합니다.\n 날짜와 지역을 입력해주세요. "
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : ["강원", "경기", "경남", "경북", "광주", "대구", "부산", "서울", "세종특별자치시", "울산", "인천", "전남", "전북", "제주", "충남", "충북"
  ] 
} , 
            "type" : "날짜 대답"
        }

    elif content ==u"미세먼지 조회" in content:
        dataSend ={
            "message": {
                 "text" :"미세먼지 정보를 제공합니다.\n  날짜와 지역을  입력해주세요."
          }
        }

    elif content == u"축제 추천" in content:
        dataSend = {
            "message": {
                "text": "먼저 야외활동에 적합한 날씨인지 확인하겠습니다.\n 날짜와 지역을 입력해주세요."
            }
        }
    
    elif content == u"옷차림 추천"  in content:
        dataSend = {
            "message": {
                "text": "먼저 날씨를 확인하겠습니다. \n 날짜와 지역을 입력해주세요."
            }
        }
    elif u"날짜, 지역" in content:
        datasend = {
            "message": {
		"text" :" 데이터보이기"
	    }
	}
    else:
        dataSend = {
            "message": {
                "text": ""
            }
        }
 
    return jsonify(dataSend)
 
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
