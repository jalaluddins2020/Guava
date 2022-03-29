from sre_constants import SUCCESS
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS

import os, sys
from os import environ
from numpy import record

import requests
from invokes import invoke_http

import json
import paypalrestsdk

app = Flask(__name__)
CORS(app)

listing_url = "http://localhost:5001/listing"
payment_records_url = "http://localhost:5006/records"
listing_update_url = "http://localhost:5001/listing"
client_id = os.getenv("PAYPAL_CLIENT_ID")
client_secret = os.getenv("PAYPAL_CLIENT_SECRET")


paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or production
    "client_id": client_id,
    "client_secret": client_secret })

@app.route("/payment") #, methods=["post"]
def start():
    global price, name, customer_id, details, listing_id, talent_id
    # receive listing_id post from customer ui
    # listing_id = request.json.get("listing_id", None)
    listing_id = 1
    listing_id = str(listing_id)

    #invoke listing microservice
    listing = invoke_http(listing_url + "/" + listing_id, method='GET')
    code = listing["code"]
    print(code)

    #listing microservice price, name & details
    if code in range(200, 300):
        price = str(listing["data"]["price"])
        name = str(listing["data"]["name"])
        customer_id = str(listing["data"]["customerID"])
        details = str(listing["data"]["details"])
        talent_id = str(listing["data"]["talentID"])
        return render_template("index.html")

    else:
        return {
            "code": 500,
            "data": {"result": listing},
            "message": "Failed to invoke listing microservice"
        }
    

@app.route("/payment/create", methods=["POST"]) 
def create():
    global price, name, customer_id, details, listing_id

    #payment creation to send to paypal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5001/payment/completed",
            "cancel_url": "http://localhost:5001/payment/cancelled"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": name, #name
                    "sku": "none",
                    "price": price, #price
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": price, #price
                "currency": "SGD"},
            "description": details }]}) #details

    if payment.create():
        print(payment)
    else:
        print(payment.error)

    return jsonify({"paymentID": payment.id})

#for onApproval
@app.route("/payment/execute", methods=["POST"])
def execute():
    global price, name, customer_id, details, listing_id

    payment = paypalrestsdk.Payment.find(request.form["paymentID"])

    if payment.execute({"payer_id": request.form["payerID"]}):
        print("Execution Success")
    else:
        print(payment.error)
    
    status = payment.success()
    print(status)

    

    # if status:
    #     body = {"payment_id": payment.id, "listing_id": 12, "customer_id": 5, "price": 15.00}
    #     record_status = invoke_http(payment_records_url, method="post", json=body)
    #     print(record_status)

    #if status is true, add to payment_records db
    if status:
        body = {"payment_id": payment.id, "listing_id": listing_id, "customer_id": customer_id, "price": price}
        record_status = invoke_http(payment_records_url, method="post", json=body)

        if record_status["code"] in range (200, 300):
            print("Sent to payment_records microservice")
        else:
            print("Record failed")

        update_status = invoke_http(listing_update_url + "/" + listing_id + "/" + talent_id, method="put",json={"listing_id": listing_id, "payment_status": "Paid"})
        if update_status["code"] in range (200, 300):
            print("Sent to listing microservice")
        else:
            print("Update to listing microservice failed")

    #payment.id will be transaction id for logging purposes in payment records
    return jsonify({"status": payment.success(), "payment": body})

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for PayPal checkout")
    app.run(host="0.0.0.0", port=5005, debug=True)



