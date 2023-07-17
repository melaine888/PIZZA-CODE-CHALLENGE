#!/usr/bin/env python3

from flask import Flask, make_response,request, make_response
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify

from models import db, Restaurant, Pizza, RestaurantPizza

api = Api(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        data = [{
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        } for restaurant in restaurants]
        return jsonify(data)

class RestaurantResource(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404
        data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            } for pizza in restaurant.pizzas]
        }
        return jsonify(data)

    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        data = [{
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        } for pizza in pizzas]
        return jsonify(data)

class RestaurantPizzaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price must be a float between 1 and 30')
    parser.add_argument('pizza_id', type=int, required=True, help='Pizza ID is required')
    parser.add_argument('restaurant_id', type=int, required=True, help='Restaurant ID is required')

    def post(self):
        args = self.parser.parse_args()
        price = args['price']
        pizza_id = args['pizza_id']
        restaurant_id = args['restaurant_id']

        if not (1 <= price <= 30):
            return jsonify({'errors': ['Price must be between 1 and 30']}), 400

        pizza = Pizza.query.get(pizza_id)
        if pizza is None:
            return jsonify({'errors': ['Pizza not found']}), 404

        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            return jsonify({'errors': ['Restaurant not found']}), 404

        restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
        db.session.add(restaurant_pizza)
        db.session.commit()

        data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        return jsonify(data), 201

api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:restaurant_id>')
api.add_resource(PizzaListResource, '/pizzas')
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas')



if __name__ == '__main__':
    app.run(port=5555)
