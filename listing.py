# Imports
#from asyncio.windows_events import NULL
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import graphene
# from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# from flask_graphql import GraphQLView
import facebook
# from graphql import Undefined
# from graphql_relay.node.node import from_global_id
from datetime import datetime
from os import environ

# initializing our app
app = Flask(__name__)
app.debug = True

CORS(app)

# Configs
# Our database configurations will go here
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:3306/listing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# Modules
# SQLAlchemy will be initiated here
db = SQLAlchemy(app)

# Models
# Our relations will be setup here
class ListingModel(db.Model):
    __tablename__ = 'listing'

    listingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerID = db.Column(db.Integer, nullable=False)
    talentID = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(300), nullable=False)
    details = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float(), nullable=False) 
    paymentStatus = db.Column(db.String(300), nullable=True)
    dateCreated = db.Column(db.DateTime(), nullable=False)

    def __init__(self, customerID, name, details, status, price, paymentStatus):
        self.customerID = customerID
        self.name = name
        self.details = details
        self.status = status
        self.price = price
        self.paymentStatus = paymentStatus

    def json(self):
        return {"listingID": self.listingID, 
                "customerID": self.customerID, 
                "talentID": self.talentID, 
                "name": self.name, 
                "details": self.details,
                "status": self.status, 
                "price": self.price, 
                "paymentStatus": self.paymentStatus, 
                "dateCreated": self.dateCreated}

#Get ALL listings (Regardless of status)
viewAllListing = "query { allListings { edges { node  {name}} } }"
@app.route("/listing")
def get_all_listing():
    listingList = ListingModel.query.all()
    if len(listingList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "listings": [listing.json() for listing in listingList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no listings."
        }
    ), 404

#Get one listing by listingID
@app.route("/listing/<string:listingID>")
def find_by_listingID(listingID):
    listing = ListingModel.query.filter_by(listingID=listingID).first()
    if listing:
        return jsonify(
            {
                "code": 200,
                "data": listing.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Listing not found."
        }
    ), 404

#Get all listing by talentID
@app.route("/listing/talent/<string:talentID>")
def find_by_talentID(talentID):
    listings = ListingModel.query.filter(ListingModel.talentID == talentID).all()
    if listings:
        return jsonify(
            {
                "code": 200,
                "data": [listing.json() for listing in listings]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Listing not found."
        }
    ), 404


#Get all listing by customerID
@app.route("/listing/customer/<string:customerID>")
def find_by_customerID(customerID):
    listings = ListingModel.query.filter(ListingModel.customerID == customerID).all()
    if listings:
        return jsonify(
            {
                "code": 200,
                "data": [listing.json() for listing in listings]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Listing not found."
        }
    ), 404

#Get AVAILABLE listings only
@app.route("/listing/Available")
def get_available_listing():
    listingList = ListingModel.query.all()
    if len(listingList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "listings": [listing.json() for listing in listingList if listing.status == "Available"]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no listings."
        }
    ), 404

#Update a listing
@app.route("/listing/update/<string:listingID>", methods=['PUT'])
def update_listing(listingID):
    try:
        listing = ListingModel.query.filter_by(listingID=listingID).first()
        if not listing:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "listingID": listingID
                    },
                    "message": "Listing not found."
                }
            ), 404

        #Check if update is either to engage or paid
        data = request.get_json()
        if data:
            if data["change"] == "engage":
                listing.status = data['status']
                listing.talentID =  data['talentID']

            elif data["change"] == "payment":
                listing.paymentStatus =  data['payment']

            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": listing.json()
                }
            ), 200
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": listingID
                },
                "message": "An error occurred while updating the listing. " + str(e)
            }
        ), 500

#Create a new listing in db
@app.route("/listing/new", methods=["POST"])
def create_new():
    try:
        data = request.get_json()
        listing = ListingModel(**data) 
        db.session.add(listing)
        db.session.commit()

        # return jsonify(
        #         {
        #             "code": 201,
        #             "data": listing.json()
        #         }
        #     ), 201

        graph = facebook.GraphAPI(access_token='EAAJpiCZBvAF4BAE7ElxxwRAkErKtvGRG2tsVWwtwfC00eCldv9pNdmxw9LqNTIFnN1oEBCxALhvVEUUc9tXLzVU8dosbWHIaL6k2W5cTE4ZCztiLJuZAuOnQOrASXKQPHk5ZBTmL2DSRVIurNdZC9dMhd3JdUj4l5BZCHpiUjWCp50ZAaVEpXRoRWZAPMvItqlkZD', version="3.0")

        graph.put_object(
            parent_object=108952705097678,
            connection_name="feed",
            message = f"NEW LISTING! \nCustomerID: {listing.customerID} \nRequired: {listing.name} \nDetails: {listing.details} \nPrice: ${listing.price}"
        )

    except Exception as e: 
        return jsonify(
            {
                "code": 500,
                "data": {
                    "error": "unknown"
                },
                "message": "An error occurred creating the listing." + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": listing.json()
        }
    ), 201

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage listing ...")
    app.run(host='0.0.0.0', port=5001, debug=True)