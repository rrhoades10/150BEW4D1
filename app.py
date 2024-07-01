from flask import Flask, request, jsonify # lets instantiate our app as an instance of Flask
from flask_marshmallow import Marshmallow #create a schema (shape) for the incoming and outgoing data
from marshmallow import fields, ValidationError #creates fields for each column that we need for incoming and outgoing data
from connection import connect_db
from mysql.connector import Error


app = Flask(__name__) #instantiates the Flask app
ma = Marshmallow(app) #creates an instance of the Marshmallow class and gives us schema functionality
# we create an instance of a flask application and pass in the current file name as its location
# __name__ current file 

# decorator from flask that applies the functionality of the following function
# to this locatio in our browser 
# / --> home page - dndbeyond.com/
@app.route("/")
def home(): #functionality at the above location 
    # also what gets rendered at that location
    print("This will show up in my terminal")
    return "<h1>Hello There! Thanks for checkin out our Flask API. Its dope!</h1>" #returns a string that is displayed in our browser

# example of another route at a different location than the home page
@app.route("/about")
def about():
    return "<h3>This application creates customers and orders for a very neat E-commcerce application</h3>"


# Building Api Endpoints
# specific target within a web application that performs a certain function
# functions being performed are a result of specific requests being made to our application
# our endpoints - add_customer() delete_customer()

# Create
# Read/Retrieve
# Update
# Delete

# GET - Read
# POST - Create
# PUT/PATCH - Update
# DELETE - Delete


# Difference between Routes and Endpoints 
# endpoints - functionality to be executed - Elite Four/Pokemon League
# routes - means by which a user arrives each endpoint - Victory Road

# Creatign a schema for our customer objects
# Define the Customer Schema
class CustomerSchema(ma.Schema):
    # sets the fields we're expecting to receive through a request
    # set the type for each field
    # set if the field is required or not, default False
    # if the field is not provided and required=True
    # or the received type is not the type provided
    # then the data does not validate and isn't used
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True) #VARCHAR(12) 630-789-4561

    class Meta:
        # fields that are displayed (Exposed)
        fields = ("name", "email", "phone")

# instantiate our schemas
customer_schema = CustomerSchema() #schema for one single object creating(POST), updating(PUT),retrieving(GET) a single customer
customers_schema = CustomerSchema(many=True) #schema for many objects retrieving several customers

# we use the above to validate data

"""
200 – OK
Everything is working. The resource has been transmitted in the message body.

201 – CREATED
A new resource has been created.

204 – NO CONTENT
The resource was successfully deleted. But, no response body was transmitted

400 – BAD REQUEST
The request was invalid or cannot be served. The exact error should be explained in the error payload.

401 – UNAUTHORIZED
The request requires user authentication.

403 – FORBIDDEN
The server understood the request but is refusing it or the access is not allowed.

404 – NOT FOUND
There is no resource behind the URI.

500 – INTERNAL SERVER ERROR API
If an error occurs in the global catch blog, the stack trace should be logged and not returned as a response.

"""
# JSON - JavaScript Object Notation
# A text format for the transfer of objects built of properties and values
# Property == key
# value == value

# Routes for each request
# GETting all Customers
#        route to the endpoint     methods that are allowed at this location
@app.route('/customers', methods=["GET"])
def get_customers():
    # connect to our database
    conn = connect_db()
    cursor = conn.cursor(dictionary=True) #returns rows of data back as dictionaries
    # the column name is the key, the data is the value



    # SQL Query to fetch all customers
    query = "SELECT * FROM Customers"
    
    # executing the query
    cursor.execute(query)

    # sets the results of our query
    customers = cursor.fetchall()
    print(customers)

    # close the connection and cursor
    cursor.close()    
    conn.close()

    # use Marshamallow schema to format our json response
    return customers_schema.jsonify(customers) #returns the dictionaries in a text form - we can see this in our browser

# ADDING A CUSTOMER - POST request
@app.route('/customers', methods=["POST"])
def add_customer():
    try: 
        # use the customer_schema to validate and deserialize the data from the request
        # this translates the json data to a python dictionary
        customer_data = customer_schema.load(request.json)
        print(request.json, "JSON DATA FROM REQUEST")
        print(customer_data, "DESERIALIZED PYTHON DICTIONARY")
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed."}), 500
        
        cursor = conn.cursor()
        name = customer_data['name']
        print(name)
        email = customer_data['email']
        print(email)
        phone = customer_data['phone']
        print(phone)

        # create new customer details based on the deserialized json data from above
        new_customer = (name, email, phone)

        # SQL Query to insert new customer into our table
        query = "INSERT INTO Customers(name, email, phone) VALUES(%s, %s, %s)"

        # execute the query
        cursor.execute(query, new_customer)
        conn.commit()

        # return a successful message for the added customer
        return jsonify({"message": "New customer added successfully"}), 201 #new resource was created
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        # closing connections
        if conn and conn.is_connected():
            cursor.close()
            conn.close()















# checkign that the file we're in is the file that is invoking the function call
if __name__ == "__main__":
    app.run(debug=True) #runs the flask application and turns the debugger on
    # debugger will point us to the location of errors in our application.
