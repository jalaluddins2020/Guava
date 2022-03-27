from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

listing_url = "http://localhost:5003/listing"
talen_url = "http://localhost:5004/talent"

@app.route("/check", methods=["post"])
def retrieve():
    # receive customer_id post from customer ui
    customer_id = request.json.get("customer_id", None)

    #invoke listing microservice
    listing = invoke_http(listing_url + "/" + customer_id, method='GET')
    code = listing["code"]
    print("listing")

    #listing microservice listingId, talentId, price, status
    if code in range (200, 300):
        listing_id = str(listing["listingID"])
        talent_id = str(listing["talentID"])
        price = str(listing["price"])
        status = str(listing["paymentStatus"])

        talent = invoke_http(listing_url + "/" + talent_id, method='GET')
        name = str(talent["name"])
        contact = str(talent["contactDetails"])
        email = str(talent["email"])

        return jsonify({
            "code": 200,
            "listing_id": listing_id,
            "name": name,
            "contact": contact,
            "email": email,
            "status": status
        })

    return jsonify({
        "code":  "404",
        "message": "Customer does not have a listing"
    })

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for PayPal checkout")
    app.run(host="0.0.0.0", port=5005, debug=True)
