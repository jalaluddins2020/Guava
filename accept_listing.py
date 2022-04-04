from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
import requests
import amqp_setup
import pika
import json

from os import environ

app = Flask(__name__)
CORS(app)

#URL
listing_URL = environ.get('listing_url') or "http://localhost:5001/listing/update"

### Accept a listing using this Complex Microservice ###
@app.route("/accept_listing/<int:listingID>",methods=['PUT'])
def accept_listing(listingID):
    if request.is_json:
        try:
            statusChange = request.get_json()
            print("\nAccepting a listing:", statusChange)

            result = processAcceptListing(statusChange,listingID)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Accept_Listing.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

### Process and perform act of accepting a listing ###
def processAcceptListing(statusChange,listingID):
    print('\n-----Invoking Listing microservice-----')
    accept_result = invoke_http(listing_URL+"/"+listingID, method='PUT', json=statusChange)
    print('accept_result:', accept_result)

    print('\n\n-----Publishing the (Accept info) message with routing_key=accept.notification-----')
    message = json.dumps(accept_result)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="accept.notification", body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print("\nNotification published to RabbitMQ Exchange.\n")
    return accept_result

if __name__ == "__main__":
    print("This is flask "+ os.path.basename(__file__) +" accepting an listing")
    app.run(host="0.0.0.0", port=5008, debug=True)  