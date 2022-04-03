# from asyncio.windows_events import NULL
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

listing_url = environ.get('listing_url') or "http://localhost:5001/listing/"
talent_url = environ.get('talent_url')  or "http://localhost:5011/talent"

@app.route("/check/<string:customer_id>")
def retrieve(customer_id):
    results = []

    #invoke listing microservice
    listing = invoke_http(listing_url + "/customer/" + customer_id, method='GET')
    code = listing["code"]

    #listing microservice listingId, talentId, price, status
    if code in range (200, 300):

        for ele in listing["data"]:

            listing_id = ele["listingID"]
            talent_id = ele["talentID"]
            price = ele["price"]
            status = ele["status"]
            paymentStatus = ele["paymentStatus"]
            title = ele["name"]
            dateCreated = ele["dateCreated"][4:16]

            talent_name = None
            contact = None
            email = None

            if talent_id != None:
                talent = invoke_http(talent_url + "/" + str(talent_id), method='GET')
                talent_name = talent["data"]["name"]
                contact = talent["data"]["contactNumber"]
                email = talent["data"]["contactEmail"]
            else:
                talent_name = "-"
                contact = "-"
                email = "-"

            results.append(
                {
                    "listingID": listing_id,
                    "name" : title,
                    "dateCreated": dateCreated,
                    "talentID": talent_id, 
                    "price": price,
                    "status": status,
                    "paymentStatus": paymentStatus,
                    "talentName": talent_name,
                    "contact": contact,
                    "email": email
                }
            )
        
        return jsonify({
            "code": 200,
            "data": results
        })

    return jsonify({
        "code":  "404",
        "message": "Customer does not have a listing"
    })

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for retrieving listings")
    app.run(host="0.0.0.0", port=5007, debug=True)
