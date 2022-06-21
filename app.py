from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# 공용 DB 선정 해서 사용 해야함~
# client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta

app = Flask(__name__)


# rendering (html 파일 넘겨주기)
@app.route('/')
def home():
    return render_template('mainpage.html')


@app.route('/header')
def header():
    return render_template('header_sunho.html')


@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/test')
def test():
    return render_template('mypage.html')


if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)