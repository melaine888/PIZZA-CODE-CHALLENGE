#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

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




if __name__ == '__main__':
    app.run(port=5501, debug=True)
