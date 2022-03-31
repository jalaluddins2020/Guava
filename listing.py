import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#import facebook

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/listing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Listing(db.Model):
    __tablename__ = 'listing'

    listingID = db.Column(db.Integer(), primary_key=True)
    customerID = db.Column(db.Integer(), nullable=False)
    talentID = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    details = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(), nullable=False) 
    paymentStatus = db.Column(db.String(300), nullable=False)
    dateCreated = db.Column(db.DateTime(), nullable=False)

    def __init__(self, listingID, customerID, talentID, name, details, status, price, paymentStatus, dateCreated):
        self.listingID = listingID
        self.customerID = customerID
        self.talentID = talentID
        self.name = name
        self.details = details
        self.status = status
        self.price = price
        self.paymentStatus = paymentStatus
        self.dateCreated = dateCreated

    def json(self):
        return {"listingID": self.listingID, "customerID": self.customerID, "talentID": self.talentID, "name": self.name, "details": self.details, "status": self.status, "price": self.price, "paymentStatus": self.paymentStatus, "dateCreated": self.dateCreated}

#Get all listings
@app.route("/listing")
def get_all_listing():
    listingList = Listing.query.all()
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

#Update a listing
@app.route("/listing/update/<string:listingID>/<string:talentID>", methods=['PUT'])
def update_listing(listingID,talentID):
    try:
        listing = Listing.query.filter_by(listingID=listingID).first()
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

        # update status
        data = request.get_json()
        if data['status']:
            listing.status = data['status']
            listing.talentID = talentID
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

#Get one listing by listingID
@app.route("/listing/<string:listingID>")
def find_by_listingID(listingID):
    listing = Listing.query.filter_by(listingID=listingID).first()
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

#Get all listing by customerID
@app.route("/listing/customer/<string:customerID>")
def find_by_customerID(customerID):
    listings = Listing.query.filter(Listing.customerID == customerID).all()
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

#Get all AVAILABLE listings only
@app.route("/listing/available")
def get_available_listing():
    listingList = Listing.query.all()
    if len(listingList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "listings": [listing.json() for listing in listingList if listing.status == "available"]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no listings."
        }
    ), 404

@app.route("/listing", methods=["POST"])
def create_new():
    if (Listing.query.filter_by(listingID=listingID).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": listingID
                },
                "message": "Listing already exists."
            }
        ), 400
    data = request.get_json()
    listing = Listing(**data) 

    try:
        db.session.add(listing)
        db.session.commit()

        graph = facebook.GraphAPI(access_token='EAAJpiCZBvAF4BAE7ElxxwRAkErKtvGRG2tsVWwtwfC00eCldv9pNdmxw9LqNTIFnN1oEBCxALhvVEUUc9tXLzVU8dosbWHIaL6k2W5cTE4ZCztiLJuZAuOnQOrASXKQPHk5ZBTmL2DSRVIurNdZC9dMhd3JdUj4l5BZCHpiUjWCp50ZAaVEpXRoRWZAPMvItqlkZD', version="3.0")

        graph.put_object(
        parent_object=108952705097678,
        connection_name="feed",
        message = f"NEW LISTING! \nCustomerID: {listing.customerID} \nRequired: {listing.name} \nDetails: {listing.details} \nPrice: ${listing.price}"
        )

    except: 
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": listingID
                },
                "message": "An error occurred creating the listing."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": listing.json()
        }
    ), 201



#create listing
@app.route("/listing/<string:listingID>", methods=['POST'])  
def create_listing(listingID):
    if (Listing.query.filter_by(listingID=listingID).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": listingID
                },
                "message": "Listing already exists."
            }
        ), 400
    data = request.get_json()
    listing = Listing(**data) 

    try:
        db.session.add(listing)
        db.session.commit()

        graph = facebook.GraphAPI(access_token='EAAJpiCZBvAF4BAE7ElxxwRAkErKtvGRG2tsVWwtwfC00eCldv9pNdmxw9LqNTIFnN1oEBCxALhvVEUUc9tXLzVU8dosbWHIaL6k2W5cTE4ZCztiLJuZAuOnQOrASXKQPHk5ZBTmL2DSRVIurNdZC9dMhd3JdUj4l5BZCHpiUjWCp50ZAaVEpXRoRWZAPMvItqlkZD', version="3.0")

        graph.put_object(
        parent_object=108952705097678,
        connection_name="feed",
        message = f"NEW LISTING! \nCustomerID: {listing.customerID} \nRequired: {listing.name} \nDetails: {listing.details} \nPrice: ${listing.price}"
        )

    except: 
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listingID": listingID
                },
                "message": "An error occurred creating the listing."
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


