from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

from json import dumps as json_encode
from flask import Flask, render_template, request, jsonify, Response
from pymongo import MongoClient

load_dotenv(join(dirname(__file__), '.env'))

client = MongoClient(environ.get("MONGODB_URI"))
database = client[environ.get("DB_NAME")]
fanbook = database.fanbook

app = Flask(__name__)

# Membenarkan: Kerusakan mixed content policy dengan membolehkan sebagian dari SpartaAPI


def allow_sparta_api(response: Response):
    response.headers["Content-Security-Policy-Report-Only"] = "default-src https: 'unsafe-inline' 'unsafe-eval' http:;"
    #response.headers["Access-Control-Allow-Origin"] = "https://lemon-sponge-puppy.glitch.me/"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route('/')
def home():
    response = Response(render_template('index.htm'))
    return allow_sparta_api(response)


@app.route("/homework", methods=["POST"])
def homework_post():
    message = request.form['message']
    nickname = request.form['nickname']
    fanbook.insert_one({
        "message": message,
        "nickname": nickname
    })
    return jsonify({
        "status": "success",
        "message": "Message posted"
    })


@app.route("/homework", methods=["GET"])
def homework_get():
    return jsonify({
        "status": "success",
        "response": list(fanbook.find({}, {'_id': False})),
        "message": "Message index"
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
