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

    #  def __init__(self, listingID, customerID, talentID, name, details, status, price, paymentStatus, dateCreated):
    #     self.listingID = listingID
    #     self.customerID = customerID
    #     self.talentID = talentID
    #     self.name = name
    #     self.details = details
    #     self.status = status
    #     self.price = price
    #     self.paymentStatus = paymentStatus
    #     self.dateCreated = dateCreated

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

# Schema Objects
# Our schema objects will go here
'''class ListingAttribute:
    customerID = graphene.Int
    talentID= graphene.Int
    name = graphene.String
    details = graphene.String
    price = graphene.Int
    status = graphene.String
    paymentStatus = graphene.String
    dateCreated = graphene.DateTime

class Listing(SQLAlchemyObjectType, ListingAttribute):
   class Meta:
       model = ListingModel
       interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    listing=graphene.relay.Node.Field(Listing)
    all_listings = SQLAlchemyConnectionField(Listing)

class AddListing(graphene.Mutation):
    class Arguments:
        customerID = graphene.Int(required=True)
        talentID= graphene.Int(required=False, default_value = "0")
        name = graphene.String(required=True) 
        details = graphene.String(required=True) 
        price = graphene.Float(required=True)
        status = graphene.String(required=False)
        paymentStatus = graphene.String(required=False)
    listing = graphene.Field(lambda: Listing)

    def mutate(self, info, talentID, customerID, name, details, price, status, paymentStatus):
        listing = ListingModel(customerID=customerID,name=name, details=details, price=price, talentID = talentID, status=status, paymentStatus=paymentStatus)
        db.session.add(listing)
        db.session.commit()
        return AddListing(listing=listing)

class Mutation(graphene.ObjectType):
    add_listing = AddListing.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Routes
# Our GraphQL route will go here
app.add_url_rule(
    '/graphql-api',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)'''

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
@app.route("/listing/available")
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
    '''if (ListingModel.query.filter_by(listingID=listingID).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "listingID": listingID
                },
                "message": "Listing already exists."
            }
        ), 400'''

    try:
        data = request.get_json()
        listing = ListingModel(**data) 
        db.session.add(listing)
        db.session.commit()

        return jsonify(
                {
                    "code": 201,
                    "data": listing.json()
                }
            ), 201

        '''graph = facebook.GraphAPI(access_token='EAAJpiCZBvAF4BAE7ElxxwRAkErKtvGRG2tsVWwtwfC00eCldv9pNdmxw9LqNTIFnN1oEBCxALhvVEUUc9tXLzVU8dosbWHIaL6k2W5cTE4ZCztiLJuZAuOnQOrASXKQPHk5ZBTmL2DSRVIurNdZC9dMhd3JdUj4l5BZCHpiUjWCp50ZAaVEpXRoRWZAPMvItqlkZD', version="3.0")

        graph.put_object(
        parent_object=108952705097678,
        connection_name="feed",
        message = f"NEW LISTING! \nCustomerID: {listing.customerID} \nRequired: {listing.name} \nDetails: {listing.details} \nPrice: ${listing.price}"
        )'''

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



#Create Facebook Listing
@app.route("/listing/<string:listingID>", methods=['POST'])  
def create_listing(listingID):
    if (ListingModel.query.filter_by(listingID=listingID).first()): 
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
    listing = ListingModel(**data) 

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


