from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

# 공용 DB 선정 해서 사용 해야함~
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

@app.route('/test')
def test():
    return render_template('mypage.html')

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 크롤링 할 페이지 url
    url = "https://www.cgv.co.kr/"
    data = requests.get(url, headers=headers)
    # beautifulSoup를 활용해서 html파일로 변경해줌
    soup = BeautifulSoup(data.text, 'html.parser')
    movie_url =soup.select_one('div.video_wrap>video >source')['src']
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


if __name__ =='__main__':
    app.run('0.0.0.0',port=5000,debug=True)