from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://team_project:sparta1234@cluster0.10xkhtt.mongodb.net/?retryWrites=true&w=majority')
db = client.team_project

app = Flask(__name__)


# rendering (html 파일 넘겨주기)
@app.route('/')
def home():
    return render_template('mainPage.html')


@app.route('/header')
def header():
    return render_template('header.html')


@app.route('/footer')
def footer():
    return render_template('footer.html')


@app.route('/movieinfo')
def test():
    post_num = request.args.get('rank')
    return render_template('sanghyun_watch.html', post_num=post_num)


# 댓글
@app.route("/comment", methods=["GET"])
def movie_comment_get():
    post_num = request.args.get('rank')
    comment_list = list(db.comment.find({'movieNum': post_num}))
    return jsonify({'comment': dumps(comment_list)})


@app.route("/comment", methods=["POST"])
def movie_post():
    textarea_receive = request.form['textarea_give']
    movieNum_receive = request.form['movieNum_give']

    bucket_list = list(db.comment.find({'movieNum': movieNum_receive}))
    count = len(bucket_list) + 1

    doc = {
        'movieNum': movieNum_receive,
        'comment': textarea_receive
    }

    db.comment.insert_one(doc)
    return jsonify({'msg': '저장완료'})


@app.route("/comment/delete", methods=["POST"])
def dlelete_comment():
    #num_receive = request.args.get('num')
    #print(num_receive)
    # db.comment.delete_one({'_id': num_receive})
    return render_template('sanghyun_watch.html')


# 영화 api
@app.route("/movieinfo/watch", methods=["POST"])
def movie_info_a():
    num_receive = request.form['rank_give']
    movie_info = db.movieDatas.find_one({'순위': num_receive}, {'_id': False})
    return jsonify({'movie_info': movie_info})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
