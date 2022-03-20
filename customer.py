from flask import Flask, request, jsonify #Import flask and initialises application
from flask_sqlalchemy import SQLAlchemy #Import flask version of SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book' #Specify database URL & use mysql+mysqlconnector prefix to instruct which database engine and connector to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #Initialise connection to database

class Customer(db.model):
    __tablename__ = 'customer'
    
    customerID = db.Column(db.Integer(1000), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    contactNumber = db.Column(db.String(64), nullable=False)
    contactEmail = db.Column(db.String(64), nullable=False)

    def __init__(self, isbn13, title, price, availability):
        self.customerID = customerID
        self.name = name
        self.contactNumber = contactNumber
        self.contactEmail = contactEmail

    def json(self):
        return {"customerID": self.customerID, "name": self.name, "contactNumber": self.contactNumber, "contactEmail": self.contactEmail}

@app.route("/customer")
def get_all_customer():
    customerlist = Customer.query.all()
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


@app.route("/customer/<string:customerID>") #Map URL route /book/isbn13 to find_by_isbn13 function, where isbn13 is a path variable of string type
def find_by_customerID(customerID):
    customer = Customer.query.filter_by(customerID=customerID).first() #Retrieve only the book with isbn13 specified in the path variable (similar to WHERE clause in SQL SELECT expression). since it returns a list of 1 book, first() is used to return 1 book/None (if no matching), which is similar to LIMIT 1 clause in SQL
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
    
"""class Book(db.Model):   #Creates new class Book -> Creates a table called book (if we run db.create_all() function)
    __tablename__ = 'book' #Specified table name as book (but possible to create/use existing table with different name from class)

    isbn13 = db.Column(db.String(13), primary_key=True) #Specify attributes which SQLAlchemy will use as column names in table. If referencing to exisiting, we are telling it about our table & columns
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability): #Specify properties of a Book when it is created
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self): #Specify how to represent our book object as a JSON string
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}*/"""


"""@app.route("/book") #Map URL route /book to get_all function
def get_all():
    booklist = Book.query.all() #A query attribute to retrieve all records from Book table. Returns a list that is assigned to "booklist"
    if len(booklist): #IF book list not empty
        return jsonify( #Returns a list of bookis in the JSON representation
            {
                "code": 200,
                "data": {
                    "books": [book.json() for book in booklist] #For loop to perform an iteration and create a JSON representation of it using book.json()
                }
            }
        )
    return jsonify( #ELSE, return an error message in JSON & return HTTP status code 404 for NOT FOUND. Unspecified will return 200 OK
        {
            "code": 404,
            "message": "There are no books."
        }
    ), 404"""


"""@app.route("/book/<string:isbn13>") #Map URL route /book/isbn13 to find_by_isbn13 function, where isbn13 is a path variable of string type
def find_by_isnb13(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first() #Retrieve only the book with isbn13 specified in the path variable (similar to WHERE clause in SQL SELECT expression). since it returns a list of 1 book, first() is used to return 1 book/None (if no matching), which is similar to LIMIT 1 clause in SQL
    if book: #IF book found (not None), return JSON representation
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify( #ELSE, return an error message in JSON & return HTTP status code 404 for NOT FOUND. Unspecified will return 200 OK
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404"""


"""@app.route("/book/<string:isbn13>", methods=['POST'])  #Map URL route /book/isbn13 to create_book function, where isbn13 is a path variable of string type. GET is the default method, have to specify other methods by passing in via methods parameter
def create_book(isbn13):
    if (Book.query.filter_by(isbn13=isbn13).first()): #Check if bok already exist in table. If yes, return an error message in JSON with HTTP status code 400 BAD REQUEST
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

    data = request.get_json() #Get data from the request received
    book = Book(isbn13, **data) #Create an instance of a book class using isbn13 and attributes sent in the request (**data)

    try:
        db.session.add(book) #Try add the book to the table and commit the change
        db.session.commit()
    except: #Returns error message in JSON with HTTP status code 500 - INTERNAL SERVER ERROR if excpetion occurs
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify( #Return JSON representation of the book that is added with HTTP status code 201 - CREATED
        {
            "code": 201,
            "data": book.json()
        }
    ), 201"""


if __name__ == '__main__':
    app.run(port=5000, debug=True) #Ensures file only start if we run this file explicitly