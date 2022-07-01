from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# 공용 DB 선정 해서 사용 해야함~
# client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta

app = Flask(__name__)

# 크롤링임포트
import requests
from bs4 import BeautifulSoup

#db연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.if3gw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# rendering (html 파일 넘겨주기)
@app.route('/')
def home():
    return render_template('mainPage.html')


@app.route('/header')
def header():
    return render_template('header_hyunjee.html')


@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route("/login", methods=["POST"])
def login():
    # id,pw_give 를 받아와서 doc (db에 저장)
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    doc = {
        'id': id_receive,
        'pw': pw_receive,
    }
    db.login.insert_one(doc)
    return jsonify({'msg': '회원가입을 축하드립니다! '
})


if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)