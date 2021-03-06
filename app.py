from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId

# 크롤링임포트
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urllib3

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


@app.route('/movieInfo')
def test():
    post_num = request.args.get('rank')
    return render_template('sanghyun_watch.html', post_num=post_num)


@app.route('/ticketing')
def tiketing():
    return render_template('Sunho/ticketing.html')


@app.route("/buy", methods=["POST"])
def buy():
    seat_receive = request.form['seat_give']
    time_receive = request.form['time_give']
    title_receive = request.form['title_give']

    if seat_receive == "":
        return jsonify({'msg': '좌석을 선택해주세요'})

    if time_receive == "":
        return jsonify({'msg': '상영시간을 선택해주세요'})

    movie_list = list(
        db.movie.find({"seat": seat_receive, "time": time_receive, "title": title_receive}, {'_id': False}))
    count = len(movie_list)
    if count > 0:
        return jsonify({'msg': '이미 예매된 좌석입니다.'})

    doc = {
        'seat': seat_receive,
        'time': time_receive,
        'title': title_receive
    }
    db.movie.insert_one(doc)

    return jsonify({'msg': '예매 완료!'})


@app.route("/join", methods=["POST"])
def join():
    # id,pw_give 를 받아와서
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    if id_receive == "":
        return jsonify({'msg': '이메일을 입력해주세요'})

    join_list = list(
        db.login.find({"id": id_receive}, {'_id': False}))
    count = len(join_list)
    if count > 0:
        return jsonify({'msg': ' 중복된 아이디입니다. '})

    #db에저장
    doc = {
        'id': id_receive,
        'pw': pw_receive,
    }
    db.login.insert_one(doc)
    return jsonify({'msg': '회원가입을 축하드립니다! '
                    })

@app.route("/login", methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    if id_receive == "":
        return jsonify({'msg': '아이디를 입력해주세요 '})

    login_list = list(
        db.login.find({"id": id_receive, "pw" : pw_receive }, {'_id': False}))
    count = len(login_list)
    if count > 0:
        return jsonify({'msg': ' 님 환영합니다 ! '})


@app.route("/loginpage")
def loginpage():
    return render_template('login.html')

@app.route("/signuppage")
def signuppage():
    return render_template('signup.html')



@app.route('/crawling_movie', methods=['GET'])
def crawling_movie():
    doc = get_movie_data()
    movie_url = crawling()
    doc.append({'movie_url': movie_url})
    return jsonify(doc)


# @app.route('/movieInfo', methods=['GET'])
# def movie_info():
#     print(request.args.get('rank'))

def get_movie_data():
    movie_data = list(db.movieDatas.find({}, {"_id": False}))
    return movie_data


def crawling():

    # 크롤링 관련
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    url = "https://www.cgv.co.kr/"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    # 크롤링 할 페이지 url
    data = requests.get(url, verify=False)

    # data = requests.get(url,  headers=headers,verify=False)
    # beautifulSoup를 활용해서 html파일로 변경해줌
    soup = BeautifulSoup(data.text, 'html.parser')
    movie_url = soup.select_one('div.video_wrap>video >source')['src']
    # print(soup)
    # recent_movies = soup.select('div.swiper-slide-movie')
    # doc = []
    # for movie in recent_movies:
    #     image = movie.select_one('div.img_wrap>img')['src']
    #     title = movie.select_one('div.img_wrap>img')['alt']
    #     movie_info = movie.select_one('div.movie_info_wrap')
    #     booking_rate = list(movie_info.stripped_strings)[2]
    #     movie_data = {'title': title, 'image': image, 'booking_rate': booking_rate}
    #     doc.append(movie_data)
    return movie_url


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


@app.route("/movieInfo", methods=["POST"])
def dlelete_comment():
    num_receive = request.args.get('id')
    post_num = request.args.get('rank')
    db.comment.delete_one({'_id': ObjectId(num_receive)})
    return render_template('sanghyun_watch.html', post_num=post_num)


# 영화 api
@app.route("/movieinfo/watch", methods=["POST"])
def movie_info_a():
    num_receive = request.form['rank_give']
    movie_info = db.movieDatas.find_one({'순위': num_receive}, {'_id': False})
    return jsonify({'movie_info': movie_info})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
