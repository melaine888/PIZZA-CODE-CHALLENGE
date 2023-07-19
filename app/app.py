#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
import sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/Home')
def home():
    return '<h2>Flask app for Restaurants</h2>'

@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_info = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_info)
    return jsonify(restaurant_list)

@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    restaurant_info = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'pizzas': []
    }
    for pizza in restaurant.pizzas:
        pizza_info = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        restaurant_info['pizzas'].append(pizza_info)
    
    return jsonify(restaurant_info)

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    # Delete associated RestaurantPizza entries
    RestaurantPizza.query.filter_by(restaurant_id=id).delete()

    # Delete the restaurant
    db.session.delete(restaurant)
    db.session.commit()

    return '', 204

@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []
    for pizza in pizzas:
        pizza_info = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_info)
    return jsonify(pizza_list)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
        return jsonify({'errors': ['validation errors']}), 400

    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']

    pizza = Pizza.query.get(pizza_id)
    if pizza is None:
        return jsonify({'error': 'Pizza not found'}), 404

    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404


if __name__ == '__main__':
    app.run(port=5501, debug=True)
