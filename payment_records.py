#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from invokes import invoke_http
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/payment_recordsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Payment_records(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.String(128), primary_key=True)
    listing_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    talent_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, payment_id, listing_id, customer_id, talent_id, price, date_time):
        self.payment_id = payment_id
        self.listing_id = listing_id
        self.customer_id = customer_id
        self.talent_id = talent_id
        self.price = price
        self.date_time = date_time

    def json(self):
        return {"payment_id": self.payment_id, "listing_id": self.listing_id, "customer_id": self.customer_id, "talent_id": self.talent_id, "price": self.price, "date_time": self.date_time}


@app.route("/records")
def get_all():
    payments = Payment_records.query.all()

    if len(payments) != 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payments": [payment.json() for payment in payments]
                }
            }
        )
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no payment records."
        }
    ), 404   


@app.route("/records/<int:param>")
def find_by_listing_id(param):
    payment = Payment_records.query.filter_by(listing_id=param).first()

    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "data": {
                "payment_id": param
            },
            "message": "Payment record not found."
        }
    ), 404


@app.route("/records", methods=['POST'])
def create_payment():
    payment_id = request.json.get('payment_id', None)
    listing_id = request.json.get('listing_id', None)
    customer_id = request.json.get('customer_id', None)
    talent_id = request.json.get('talent_id', None)
    price = request.json.get('price', None)

    new_payment = Payment_records(payment_id, listing_id, customer_id, talent_id, price, datetime.now())

    try:
        db.session.add(new_payment)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating new payment. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_payment.json()
        }
    ), 201


if __name__ == '__main__':
    print("Initiating" + os.path.basename(__file__) + " - the payments microservice")
    app.run(host='0.0.0.0', port=5006, debug=True)
