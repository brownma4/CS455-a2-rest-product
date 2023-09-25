import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), default="4.99")
    quantity = db.Column(db.Integer, default=1) 
    user_id = db.Column(db.Integer, default=0) 

# Endpoint 1: Get all products in the database
@app.route('/products', methods=['GET'])
def get_products():

    # gets all of the products in the database
    products = Product.query.all()
    
    # creates a list of all of the products
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity, "user_id": product.user_id} for product in products]
    return jsonify({"products": product_list}), 200

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    # queries the database for products with the given id
    product = Product.query.get(product_id)

    # if a product with the given id exists, returns its info. If not, returns an error
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity, "user_id": product.user_id}})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Add a new product to the database
@app.route('/products', methods=['POST'])
def add_product():
    
    # gets the product's info
    data = request.json
    product_to_add = Product(**data)

    # gets all of the products database to see if the product already exists
    products = Product.query.all()

    # if the product already exists in the database, updates the quantity and deletes it if the quantity is 0
    for product in products:
        # if the product id is a match, updates the quantity
        if product.id == product_to_add.id or product.name == product_to_add.name:
            product.quantity = product.quantity + product_to_add.quantity
            
            # if the quantity is zero, removes it from the database
            if product.quantity == 0:
                db.session.delete(product)
                db.session.commit()
                return jsonify({"Product removed": "yay"}), 200
            
            # if the quantity is less than 0, returns an error without saving it to the database
            if product.quantity < 0:
                return jsonify({"error": "Quantity of product to remove too high"}), 400
            
            # commits the quantity update
            else:
                db.session.commit()
                return jsonify({"Product quantity updated": "yay"}), 200
    
    # if the quantity of the product is negative and the task was not found, returns an error
    if product_to_add.quantity < 0:
        return jsonify({"error": "Task not found"}), 404

    # if no instance of this product is in the database for the current user, adds it to the database
    db.session.add(product_to_add)
    db.session.commit()

    return jsonify({"message": "Product added", "product": {"id": product_to_add.id, "name": product_to_add.name, "price": product_to_add.price, "quantity": product_to_add.quantity, "user_id": product_to_add.user_id}}), 201


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host="0.0.0.0", port=10000)
