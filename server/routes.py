from .models import db, Restaurant, RestaurantPizza, Pizza
from flask import Blueprint, jsonify, request

routes_bp = Blueprint("routes_bp", __name__)

# Get all restaurants
@routes_bp.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
@routes_bp.route("/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    restaurant_data = restaurant.to_dict()
    restaurant_data["restaurant_pizzas"] = [rp.to_dict() for rp in restaurant.restaurant_pizzas]
    return jsonify(restaurant_data), 200
@routes_bp.route("/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()
    return '', 204
@routes_bp.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([p.to_dict() for p in pizzas]), 200
@routes_bp.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        new_rp = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(new_rp)
        db.session.commit()

        return jsonify(new_rp.to_dict()), 201

    except Exception:
        return jsonify({"errors": ["validation errors"]}), 400