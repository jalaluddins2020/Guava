import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/listing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

"""
Missing Functions:
    1. Get listing by ID
    2. Get listings that are only available (to show to talent)
    3. idk what else
    
"""

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

    def __init__(self, listingID, customerID, talentID, name, details, status, price, paymentStatus):
        self.listingID = listingID
        self.customerID = customerID
        self.talentID = talentID
        self.name = name
        self.details = details
        self.status = status
        self.price = price
        self.paymentStatus = paymentStatus

    def json(self):
        return {"listingID": self.listingID, "customerID": self.customerID, "talentID": self.talentID, "name": self.name, "details": self.details, "status": self.status, "price": self.price, "paymentStatus": self.paymentStatus}

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
@app.route("/listing/<string:listingID>/<string:talentID>", methods=['PUT'])
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

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage listing ...")
    app.run(host='0.0.0.0', port=5001, debug=True)


