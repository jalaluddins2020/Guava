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

listing_url = "http://localhost:5003/listing"
payment_records_url = "http://localhost:5002/records"
listing_update_url = "http://localhost:5003/listing"


paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or production
    "client_id": "AT2PB40zeSiziVMaCuxMdg9pafOBAMYXu36luQKlpsZLEWsIuReMMD53-BGrSq9vlgqCGujOAb9aomwH",
    "client_secret": "ELx7FSv-nQTDeHkNHJ9pmtaZLQzcDVLFa8cmIBUWN5aw795LeSOB6_ZV4VUB5qwX9WPq0HkoaCCjgon-" })

@app.route("/payment") #, methods=["post"]
def start():
    global price, name, customer_id, details, listing_id
    # # receive listing_id post from customer ui
    # listing_id = request.json.get("listing_id", None)

    # #invoke listing microservice
    # listing = invoke_http(listing_url + "/" + listing_id, method='GET')
    # code = listing["code"]
    # print("listing")

    # #listing microservice price, name & details
    # if code in range(200, 300):
        # price = str(listing["price"])
        # name = str(listing["name"])
        # customer_id = str(listing["customerID"])
        # details = str(listing["details"])
    return render_template("index.html")

    # else:
        # return {
        #     "code": 500,
        #     "data": {"result": listing},
        #     "message": "Failed to invoke listing microservice"
        # }
    

@app.route("/payment/create") 
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
                    "name": "services_placeholder", #name
                    "sku": "none",
                    "price": "25.00", #price
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": "25.00", #price
                "currency": "SGD"},
            "description": "placeholder" }]}) #details

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

    #if status is true, add to payment_records db
    # if status:
    #     body = {"payment_id": payment.id, "listing_id": listing_id, "customer_id": customer_id, "price": price}
    #     invoke_http(payment_records_url, method="post", json=body)

    if status:
        body = {"payment_id": payment.id, "listing_id": 12, "customer_id": 5, "price": 15.00}
        record_status = invoke_http(payment_records_url, method="post", json=body)
        print(record_status)

        if record_status["code"] in range (200, 300):
            print("Sent to payment_records microservice")
        else:
            print("Record failed")

        # update_status = invoke_http(listing_update_url + "/" + listing_id, method="put",json={"listing_id": listing_id, "payment_status": "Paid"})
        # if update_status["code"] in range (200, 300):
        #     print("Sent to listing microservice")
        # else:
        #     print("Update to listing microservice failed")

    #payment.id will be transaction id for logging purposes in payment records
    return jsonify({"status": payment.success(), "payment": body})

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for PayPal checkout")
    app.run(host="0.0.0.0", port=5001, debug=True)



