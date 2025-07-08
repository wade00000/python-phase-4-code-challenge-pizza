from flask import Blueprint, request, jsonify
from models import db, Restaurant, Pizza, RestaurantPizza

app = Blueprint('api', __name__)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    data = [
        { 'id': r.id, 'name': r.name, 'address': r.address }
        for r in Restaurant.query.all()
    ]
    return jsonify(data), 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    r = Restaurant.query.get(id)
    if not r:
        return jsonify({"error": "Restaurant not found"}), 404

    result = {
        'id': r.id,
        'name': r.name,
        'address': r.address,
        'restaurant_pizzas': [
            {
                'id': rp.id,
                'price': rp.price,
                'pizza_id': rp.pizza_id,
                'restaurant_id': rp.restaurant_id,
                'pizza': {
                    'id': rp.pizza.id,
                    'name': rp.pizza.name,
                    'ingredients': rp.pizza.ingredients
                }
            } for rp in r.restaurant_pizzas
        ]
    }
    return jsonify(result), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    r = Restaurant.query.get(id)
    if not r:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(r)
    db.session.commit()
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    data = [
        {'id': p.id, 'name': p.name, 'ingredients': p.ingredients}
        for p in Pizza.query.all()
    ]
    return jsonify(data), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def add_restaurant_pizza():
    data = request.get_json()
    try:
        price = int(data.get('price'))
    except (TypeError, ValueError):
        return jsonify({"errors": ["validation errors"]}), 400

    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    
    if price < 1 or price > 30:
        return jsonify({"errors": ["validation errors"]}), 400

    rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(rp)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    result = {
        'id': rp.id,
        'price': rp.price,
        'pizza_id': rp.pizza_id,
        'restaurant_id': rp.restaurant_id,
        'pizza': {
            'id': rp.pizza.id,
            'name': rp.pizza.name,
            'ingredients': rp.pizza.ingredients
        },
        'restaurant': {
            'id': rp.restaurant.id,
            'name': rp.restaurant.name,
            'address': rp.restaurant.address
        }
    }
    return jsonify(result), 201
