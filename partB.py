
from flask import Flask, request, jsonify
import sqlite3 as sql
from flask import render_template

app = Flask(__name__)

# load the dataset data\steam_modified.csv, and load it into a dataset manageable by sqllite
# create a connection to the database
conn = sql.connect('data.db')
# create a cursor object
cur = conn.cursor()
cur.execute("""drop table if exists products""")
# Create a table in the database to store the dataset
cur.execute("""drop table if exists orders""")

cur.execute('''drop table if exists cart''')

# create table product
cur.execute("""CREATE TABLE products(
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    category TEXT,
    stock INTEGER)""")
# create table order
cur.execute("""CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total REAL)""")

# create table cart
cur.execute("""CREATE TABLE cart(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER)""")

# Commit the changes and close the connection
conn.commit()
conn.close()

# Define the routes

# Route to retrieve a list of all products
@app.route('/products', methods=['GET'])
def get_products():
    conn = sql.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return jsonify(products)

# Route to fetch detailed information about a specific product
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = sql.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cur.fetchone()
    conn.close()
    return jsonify(product)

# Route to add a new product to the store
@app.route('/products', methods=['POST'])
def add_product():
    conn = sql.connect('data.db')
    # Extract the product information from the request body
    product_info = request.json
    # Implement the logic to add the new product to the store
    # and return the details of the newly added product
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)",
                (product_info['name'], product_info['price'], product_info['category'], product_info['stock']))
    conn.commit()
    created_product = cur.execute("SELECT * FROM products WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(created_product)

# Route to update the details of an existing product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    conn = sql.connect('data.db')
    # Extract the updated product information from the request body
    updated_product_info = request.json
    # Implement the logic to update the product in the store
    # and return the updated details of the product
    cur = conn.cursor()
    cur.execute("UPDATE products SET name=?, price=?, category=?, stock=? WHERE id=?",
                (updated_product_info['name'], updated_product_info['price'], updated_product_info['category'], updated_product_info['stock'], id))
    conn.commit()
    updated_product = cur.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return jsonify(updated_product)

# Route to remove a product from the store
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = sql.connect('data.db')
    # Implement the logic to remove the product
    # identified by its ID from the store
    # and return a confirmation message
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})

# Route to create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    conn = sql.connect('data.db')
    # Extract the order information from the request body
    order_info = request.json
    # Implement the logic to create a new order with selected products
    # and return detailed information of the created order
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)",
                (order_info['user_id'], order_info['total']))
    conn.commit()
    conn.close()
    created_order = cur.execute("SELECT * FROM orders WHERE id=?", (cur.lastrowid,)).fetchone()

    return jsonify(created_order)

# Route to retrieve all orders placed by a specific user
@app.route('/orders/<int:userId>', methods=['GET'])
def get_user_orders(userId):
    conn = sql.connect('data.db')
    # Implement the logic to retrieve all orders placed by the user
    # identified by the user ID and return an array of orders
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id=?", (userId,))
    user_orders = cur.fetchall()
    conn.close()
    return jsonify(user_orders)

# Route to add a product to the user's shopping cart
@app.route('/cart/<int:userId>', methods=['POST'])
def add_to_cart(userId):
    conn = sql.connect('data.db')
    # Extract the product information from the request body
    product_info = request.json
    # Implement the logic to add the product to the user's shopping cart
    # and return the updated contents of the cart
    cur = conn.cursor()
    cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (userId, product_info['product_id'], product_info['quantity']))
    conn.commit()
    updated_cart = cur.execute("SELECT * FROM cart WHERE user_id=?", (userId,)).fetchall()
    conn.close()
    return jsonify(updated_cart)

# Route to retrieve the current state of a user's shopping cart
@app.route('/cart/<int:userId>', methods=['GET'])
def get_cart(userId):
    conn = sql.connect('data.db')
    # Implement the logic to retrieve the current state of the user's shopping cart
    # and return a JSON object listing the products in the cart, their quantities, and the total price
    cur = conn.cursor()
    cur.execute("SELECT * FROM cart WHERE user_id=?", (userId,))
    cart_contents = cur.fetchall()
    conn.close()
    return jsonify(cart_contents)

# Route to remove a specific product from the user's shopping car
@app.route('/cart/<int:userId>/item/<int:productId>', methods=['DELETE'])
def remove_from_cart(userId, productId):
    conn = sql.connect('data.db')
    # Implement the logic to remove the specified product from the user's shopping cart
    # and return the updated contents of the cart
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id=? AND product_id=?", (userId, productId))
    conn.commit()
    updated_cart = cur.execute("SELECT * FROM cart WHERE user_id=?", (userId,)).fetchall()
    conn.close()
    return jsonify(updated_cart)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Route to get server status
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
    app.run(debug=True, host='localhost', port=5000)

