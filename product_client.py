import requests
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), default="4.99")
    quantity = db.Column(db.Integer, default=1) 
    user_id = db.Column(db.Integer, default=0) 
    
# lists all the products in the database
def get_all_products():
    response = requests.get('http://127.0.0.1:5000/products')
    data = response.json()
    return data

# gets the info of a product from its unique id
def get_product(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    data = response.json()
    return data

# adds product to database
def add_product(product):
    new_product = {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity, "user_id": 0}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    data = response.json()
    return data


if __name__ == '__main__':
    
    # gets the initial inventory
    all_products = get_all_products()
    print("All Product:")
    print(all_products)

    # adds strawberries to user 2's cart
    strawberries = Product(id = 1, name="strawberries", price="3.99", quantity=2, user_id=0)
    added_product = add_product(strawberries)
    print(f"\nAdded_product:")
    print(added_product) 
    
    # checks the product of id = 3
    product_id = 3
    specific_product = get_product(product_id)
    print(f"\nProduct {product_id}:")
    print(specific_product)

    # adds cereal to database
    cereal = Product(id = 2, name="Cereal", price="5.99", quantity=1, user_id=0)
    added_product = add_product(cereal)
    print(f"\nAdded_product:")
    print(added_product)

    # adds bananas to database
    bananas = Product(name="bananas", price="0.99", quantity=4, user_id=0)
    added_product = add_product(bananas)
    print(f"\nAdded_product:")
    print(added_product)

    # adds milk to database
    milk = Product(name="milk", price="4.99", quantity=2, user_id=0)
    added_product = add_product(milk)
    print(f"\nAdded_product:")
    print(added_product)

    # gets the updated inventory
    all_products = get_all_products()
    print(f"\nAll Products:")
    print(all_products)