from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref='restaurants')
    
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('restaurant_pizza', lazy=True))
    pizza = db.relationship('Pizza', backref=db.backref('restaurant_pizza', lazy=True))    