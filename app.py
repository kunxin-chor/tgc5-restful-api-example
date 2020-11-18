from flask import Flask, render_template, request, redirect, url_for, Response
from dotenv import load_dotenv
import pymongo
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
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
    movies = client[DB_NAME].movies.find()
    return dumps(movies)


@app.route('/movie/<movie_id>', methods=['GET'])
@cross_origin()
def get_detail(movie_id):
    client = get_connection()
    movies = client[DB_NAME].movies.find_one({
        "_id": ObjectId(movie_id)
    })
    return dumps(movies)


@app.route('/movie/create', methods=["POST"])
@cross_origin()
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
        # get the new ID of the movie from the insert result
        'new_id': insert_result.inserted_id
    }), status=200, mimetype="application/json")


@app.route('/movie/<movie_id>', methods=['PATCH'])
@cross_origin()
def update_movie(movie_id):
    title = request.json.get('title')
    plot = request.json.get('plot')

    client = get_connection()

    client[DB_NAME].movies.update_one({
        '_id': ObjectId(movie_id)
    }, {
        "$set": {
            'title': title,
            'plot': plot
        }
    })

    return Response(dumps({
        'status': 'ok',
        'updated_id': movie_id
    }), status=200, mimetype="application/json")


@app.route('/movie/<movie_id>', methods=['DELETE'])
@cross_origin()
def delete_movie(movie_id):
    client = get_connection()

    client[DB_NAME].movies.remove({
        '_id': ObjectId(movie_id)
    })

    return Response(dumps({
        'status': 'ok',
        'deleted_id': movie_id
    }), status=200, mimetype="application/json")


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
