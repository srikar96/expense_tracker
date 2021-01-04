import requests
from flask import Flask
from flask import request
import json
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There You!</h1>"

@app.route("/rasa", methods = ['POST'])
def rasa():
    data = request.get_json()

    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json = {"sender": data["sender"], "message": data["text"]}).json()
    
    #return "<h1 style='color:red'>Hello {}!</h1>".format(response[0]['text'])
    return jsonify(response[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
