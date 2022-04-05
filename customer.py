import os
from flask import Flask, request, jsonify #Import flask and initialises application
from flask_sqlalchemy import SQLAlchemy #Import flask version of SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:3306/customer' #Specify database URL & use mysql+mysqlconnector prefix to instruct which database engine and connector to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app) #Initialise connection to database

CORS(app)  

#Declare Model
class CustomerModel(db.Model):
    __tablename__ = 'customer'
    
    customerID = db.Column(db.Integer(), primary_key=True, autoincrement = True)
    name = db.Column(db.String(300), nullable=False)
    contactNumber = db.Column(db.Integer(), nullable=False)
    contactEmail = db.Column(db.String(300), nullable=False)

    def __init__(self, name, contactNumber, contactEmail):
        self.name = name
        self.contactNumber = contactNumber
        self.contactEmail = contactEmail

    def json(self):
        return {"name": self.name, "contactNumber": self.contactNumber, "contactEmail": self.contactEmail}

### Get all talent details ###
@app.route("/customer")
def get_all_customer():
    customerlist = CustomerModel.query.all()
    if len(customerlist):
        return jsonify(
            {
                "code": 200,
                "data":{
                    "customers": [customer.json() for customer in customerlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no customer records."
        }
    ), 404

### Get one talent detail by a customerID ###
@app.route("/customer/<int:customerID>") #Map URL route /book/isbn13 to find_by_isbn13 function, where isbn13 is a path variable of string type
def find_by_customerID(customerID):
    customer = CustomerModel.query.filter_by(customerID=customerID).first() #Retrieve only the book with isbn13 specified in the path variable (similar to WHERE clause in SQL SELECT expression). since it returns a list of 1 book, first() is used to return 1 book/None (if no matching), which is similar to LIMIT 1 clause in SQL
    if customer: #IF book found (not None), return JSON representation
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify( #ELSE, return an error message in JSON & return HTTP status code 404 for NOT FOUND. Unspecified will return 200 OK
        {
            "code": 404,
            "message": "Customer not found."
        }
    ), 404

### Create a new customer record ###
@app.route("/customer", methods=['POST'])  
def create_customer():

    data = request.get_json()
    customer = CustomerModel(**data) 

    contactNumber=customer.contactNumber
    contactEmail=customer.contactEmail
    if (CustomerModel.query.filter_by(contactNumber=contactNumber).first() or CustomerModel.query.filter_by(contactEmail=contactEmail).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "contactNumber": contactNumber,
                    "contactEmail": contactEmail
                },
                "message": "Customer already exists."
            }
        ), 400

    try:
        db.session.add(customer)
        db.session.commit()
    except: 
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201    

### Authenticate talent who login ###
@app.route("/customer/authenticate/<string:customerEmail>/<int:customerNumber>")
def authenticate(customerEmail,customerNumber):
    customer = CustomerModel.query.filter(CustomerModel.contactEmail == customerEmail).filter(CustomerModel.contactNumber == customerNumber).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Talent not found."
        }
    ), 404

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": Managing Customers ...")
    app.run(host='0.0.0.0', port=5010, debug=True)
   