import os
from flask import Flask, request, jsonify #Import flask and initialises application
from flask_sqlalchemy import SQLAlchemy #Import flask version of SQLAlchemy

import requests
import json

app = Flask(__name__)

@app.route("/notify/<string:listingID>/")
def telegram_bot_sendtext(message):
    bot_token = '5195002024:AAFOVxloVJsi_NdnEh3Ex-YWJn0pWpdJB68'
    user_chatID = '121792469' #526817194
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + user_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    print(response)
    return response.json()

telegram_bot_sendtext("test message");

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": notifications ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
    telegram_bot_sendtext("test message");
