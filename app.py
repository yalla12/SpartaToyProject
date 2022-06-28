from flask import Flask, render_template, request, jsonify

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://text:sparta@cluster0.3wkhjck.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


# rendering (html 파일 넘겨주기)
@app.route('/')
def home():
    return render_template('mainPage.html')


@app.route('/header')
def header():
    return render_template('header_hyunjee.html')
4

@app.route('/footer')
def footer():
    return render_template('footer.html')


@app.route('/test')
def test():
    return render_template('sanghyun_watch.html')


# 댓글
@app.route("/comment", methods=["POST"])
def movie_post():
    textarea_receive = request.form['textarea_give']

    bucket_list = list(db.comment.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'comment': textarea_receive
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': '저장완료'})


@app.route("/comment", methods=["GET"])
def movie_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comment': comment_list})


@app.route("/comment/delete", methods=["POST"])
def dlelete_comment():
    num_receive = request.form['num_give']
    db.comment.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제완료'})


# 영화 api
@app.route("/movie/info", methods=["GET"])
def movie_api():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=81888', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    star = soup.select_one(
        '#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.netizen_score > div > div > em').text

    desc1 = soup.select_one(
        '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > h5').text
    desc2 = soup.select_one(
        '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text

    doc = {
        'image': image,
        'star': star,
        'desc2': desc2,
        'desc1': desc1,
    }
    return jsonify({'movie_info': doc})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
