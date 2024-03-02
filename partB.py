
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import pandas as pd
import os
import pickle
import tensorflow as tf
import sqlite3 as sql

# load the dataset
data  = pd.read_csv('data\steam_modified.csv', index_col=0)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# load the dataset data\steam_modified.csv, and load it into a dataset manageable by sqllite
# create a connection to the database
conn = sql.connect('data.db')
# create a cursor object
cur = conn.cursor()
# Create a table in the database to store the dataset
cur.execute('''CREATE TABLE IF NOT EXISTS steam_data (
                appid INTEGER PRIMARY KEY,
                name TEXT,
                release_date DATE,
                english INTEGER,
                developer TEXT,
                publisher TEXT,
                platforms TEXT,
                required_age INTEGER,
                categories TEXT,
                genres TEXT,
                steamspy_tags TEXT,
                achievements INTEGER,
                positive_ratings INTEGER,
                negative_ratings INTEGER,
                average_playtime INTEGER,
                median_playtime INTEGER,
                owners TEXT,
                price REAL,
                positive_ratio REAL
            )''')

# Insert the dataset into the table
for index, row in data.iterrows():
    cur.execute('''INSERT INTO steam_data (
                    appid, name, release_date, english, developer, publisher, platforms, required_age,
                    categories, genres, steamspy_tags, achievements, positive_ratings, negative_ratings,
                    average_playtime, median_playtime, owners, price, positive_ratio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (row['appid'], row['name'], row['release_date'], row['english'], row['developer'],
                 row['publisher'], row['platforms'], row['required_age'], row['categories'], row['genres'],
                 row['steamspy_tags'], row['achievements'], row['positive_ratings'], row['negative_ratings'],
                 row['average_playtime'], row['median_playtime'], row['owners'], row['price'], row['positive_ratio']))

# Commit the changes and close the connection
conn.commit()
conn.close()


def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Validate the username and password and return a 401 error if invalid
    # This is just an example, you should connect to your database to check the username and password
    if username != 'test' or password != 'test':
        return jsonify({'login': False}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Define the routes

# Route to retrieve a list of all products
@app.route('/products', methods=['GET'])
@jwt_required
def get_products():
    # Implement the logic to retrieve all products
    # and return a JSON array of products
    return jsonify(products)

# Route to fetch detailed information about a specific product
@app.route('/products/<int:id>', methods=['GET'])
@jwt_required
def get_product(id):
    # Implement the logic to fetch detailed information
    # about the product identified by its ID
    # and return a JSON object containing the details
    return jsonify(product)

# Route to add a new product to the store
@app.route('/products', methods=['POST'])
@jwt_required
def add_product():
    # Extract the product information from the request body
    product_info = request.json
    # Implement the logic to add the new product to the store
    # and return a JSON object of the created product
    return jsonify(created_product)

# Route to update the details of an existing product
@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required
def update_product(id):
    # Extract the updated product information from the request body
    updated_info = request.json
    # Implement the logic to update the details of the product
    # identified by its ID and return the updated product details
    return jsonify(updated_product)

# Route to remove a product from the store
@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required
def delete_product(id):
    # Implement the logic to remove the product
    # identified by its ID from the store
    # and return a confirmation message
    return jsonify({'message': 'Product deleted successfully'})

# Route to create a new order
@app.route('/orders', methods=['POST'])
@jwt_required
def create_order():
    # Extract the order information from the request body
    order_info = request.json
    # Implement the logic to create a new order with selected products
    # and return detailed information of the created order
    return jsonify(created_order)

# Route to retrieve all orders placed by a specific user
@app.route('/orders/<int:userId>', methods=['GET'])
@jwt_required
def get_user_orders(userId):
    # Implement the logic to retrieve all orders placed by the user
    # identified by the user ID and return an array of orders
    return jsonify(user_orders)

# Route to add a product to the user's shopping cart
@app.route('/cart/<int:userId>', methods=['POST'])
@jwt_required
def add_to_cart(userId):
    # Extract the product information from the request body
    product_info = request.json
    # Implement the logic to add the product to the user's shopping cart
    # and return the updated contents of the cart
    return jsonify(updated_cart)

# Route to retrieve the current state of a user's shopping cart
@app.route('/cart/<int:userId>', methods=['GET'])
@jwt_required
def get_cart(userId):
    # Implement the logic to retrieve the current state of the user's shopping cart
    # and return a JSON object listing the products in the cart, their quantities, and the total price
    return jsonify(cart_contents)

# Route to remove a specific product from the user's shopping car
@app.route('/cart/<int:userId>/item/<int:productId>', methods=['DELETE'])
@jwt_required
def remove_from_cart(userId, productId):
    # Implement the logic to remove the specified product from the user's shopping cart
    # and return the updated contents of the cart
    return jsonify(updated_cart)
#getserver
@app.route('/getServer', methods=['GET'])
def getServer():
    return jsonify({'server': 'Server is running'})

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({'error': 'Bad request', 'message': str(e)}), 400

@app.errorhandler(500)
def handle_server_error(e):
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    # Create an instance of the Flask class
