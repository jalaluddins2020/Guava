import os
from flask import Flask, request, jsonify #Import flask and initialises application
from flask_sqlalchemy import SQLAlchemy #Import flask version of SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/customer' #Specify database URL & use mysql+mysqlconnector prefix to instruct which database engine and connector to use
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

    def __init__(self, customerID, name, contactNumber, contactEmail):
        self.customerID = customerID
        self.name = name
        self.contactNumber = contactNumber
        self.contactEmail = contactEmail

    def json(self):
        return {"customerID": self.customerID, "name": self.name, "contactNumber": self.contactNumber, "contactEmail": self.contactEmail}

#View All Customer Data
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

#View One Customer Data By CustomerID
@app.route("/customer/<string:customerID>") #Map URL route /book/isbn13 to find_by_isbn13 function, where isbn13 is a path variable of string type
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

#Create a New Customer Record
@app.route("/customer/<string:customerID>", methods=['POST'])  
def create_customer(customerID):
    if (CustomerModel.query.filter_by(customerID=customerID).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "customerID": customerID
                },
                "message": "Customer already exists."
            }
        ), 400
    data = request.get_json()
    customer = CustomerModel(**data) 

    try:
        db.session.add(customer)
        db.session.commit()
    except: 
        return jsonify(
            {
                "code": 500,
                "data": {
                    "customerID": customerID
                },
                "message": "An error occurred creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201    

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage customers ...")
    app.run(host='0.0.0.0', port=5010, debug=True)
   