from models import db, Restaurant, Pizza , RestaurantPizza
from faker import Faker
from random import randomint ,choices as rc
from datetime import datetime
from app import app

fake = Faker()


def seed_data():
    # Start on a clean slate
    with app.app.context():
        db.create_all()
        
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    Pizza.query.delete()

    #Create Restaurant
    restaurants = [] 
    for _ in range(20):
        r = Restaurant(name=fake.company())
        restaurants.append(r)
    
    #Add data to session and commit changes
    db.session.add_all(restaurants)
    db.session.commit()

    # Create Pizza
    pizzas = []
    for i in range(50):
        p = Pizza(name=fake.word(), price=randint(1, 30), created_at=datetime.now())
        pizzas.append(p)
        
    db.session.add_all(pizzas)
    db.session.commit()
    
    # Create RestaurantPizza
    restaurant_pizzas = []
    for restaurant in restaurants:
        num_pizzas = randomint(1,5)
        sampled_pizzas = rc(pizzas, k=num_pizzas)
        
        for pizza in sampled_pizzas:
            rp = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id)
            restaurant_pizzas.append(rp)
    
    db.session.add_all(restaurants)
    db.session.commit()
    

if __name__ == '__main__':
    seed_data()        
    
