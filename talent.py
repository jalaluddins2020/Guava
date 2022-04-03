import os
from flask import Flask, request, jsonify #Import flask and initialises application
from flask_sqlalchemy import SQLAlchemy #Import flask version of SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:3306/talent' #Specify database URL & use mysql+mysqlconnector prefix to instruct which database engine and connector to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app) #Initialise connection to database

CORS(app)  

#Declare Model
class Talent(db.Model):
    __tablename__ = 'talent'
    
    talentID = db.Column(db.Integer(), primary_key=True, autoincrement = True)
    name = db.Column(db.String(300), nullable=False)
    contactNumber = db.Column(db.Integer(), nullable=False)
    contactEmail = db.Column(db.String(300), nullable=False)

    def __init__(self, talentID, name, contactNumber, contactEmail):
        self.talentID = talentID
        self.name = name
        self.contactNumber = contactNumber
        self.contactEmail = contactEmail

    def json(self):
        return {"talentID": self.talentID, "name": self.name, "contactNumber": self.contactNumber, "contactEmail": self.contactEmail}

#View All Talent Data - CONVERT TO GRAPHQL TO
@app.route("/talent")
def get_all_talents():
    talentsList = Talent.query.all()
    if len(talentsList):
        return jsonify(
            {
                "code": 200,
                "data":{
                    "customers": [talent.json() for talent in talentsList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no talent records."
        }
    ), 404

#View One Talent Data By talentID - CONVERT TO GRAPHQL
@app.route("/talent/<string:talentID>") #Map URL route /book/isbn13 to find_by_isbn13 function, where isbn13 is a path variable of string type
def find_by_talentID(talentID):
    talent = Talent.query.filter_by(talentID=talentID).first() #Retrieve only the book with isbn13 specified in the path variable (similar to WHERE clause in SQL SELECT expression). since it returns a list of 1 book, first() is used to return 1 book/None (if no matching), which is similar to LIMIT 1 clause in SQL
    if talent: #IF book found (not None), return JSON representation
        return jsonify(
            {
                "code": 200,
                "data": talent.json()
            }
        )
    return jsonify( #ELSE, return an error message in JSON & return HTTP status code 404 for NOT FOUND. Unspecified will return 200 OK
        {
            "code": 404,
            "message": "Talent not found."
        }
    ), 404

#Authenticate - REMAIN AS FLASK
@app.route("/talent/authenticate/<string:talentEmail>/<string:talentNumber>")
def authenticate(talentEmail,talentNumber):
    talent = Talent.query.filter(Talent.contactEmail == talentEmail).filter(Talent.contactNumber == talentNumber).first()
    if talent:
        return jsonify(
            {
                "code": 200,
                "data": talent.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Talent not found."
        }
    ), 404

#Create a New talent Record - CONVERT TO GRAPHQL
@app.route("/talent/<string:talentID>", methods=['POST'])  
def create_talent(talentID):
    if (Talent.query.filter_by(talentID=talentID).first()): 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "talentID": talentID
                },
                "message": "Talent already exists."
            }
        ), 400
    data = request.get_json()
    talent = Talent(**data) 

    try:
        db.session.add(talent)
        db.session.commit()
    except: 
        return jsonify(
            {
                "code": 500,
                "data": {
                    "talentID": talentID
                },
                "message": "An error occurred creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": talent.json()
        }
    ), 201    

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": Managing Talent ...")
    app.run(host='0.0.0.0', port=5011, debug=True)
   