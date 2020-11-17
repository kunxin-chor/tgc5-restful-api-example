from flask import Flask, render_template, request, redirect, url_for, Response
from dotenv import load_dotenv
import pymongo
import os
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__)
DB_NAME = 'my_movies'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



def get_connection():
    client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
    return client


@app.route('/')
@cross_origin()
def index():
    return render_template('index.template.html')


@app.route('/movies')
@cross_origin()
def show_movies():
    client = get_connection()
    movies = client[DB_NAME].movies.find().limit(10)
    return dumps(movies)


@app.route('/movie/create', methods=["POST"])
def create_movie():
    # because axios sends the data to Flask with the JSON format,
    # so we use request.json instead of request.form
    title = request.json.get('title')
    plot = request.json.get('plot')

    client = get_connection()
    insert_result = client[DB_NAME].movies.insert_one({
        'title': title,
        'plot': plot
    })

    return Response(dumps({
        'status': 'ok',
        'new_id': insert_result.inserted_id  # get the new ID of the movie from the insert result
    }), status=200, mimetype="application/json")


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
