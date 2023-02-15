#!/usr/bin/python3
"""Place module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


r3 = "cities/<city_id>/places"
r4 = "places/<place_id>"


@app_views.route(r3, methods=["GET", "POST"], strict_slashes=False)
def city_places(city_id):
    """City Places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "user_id" not in body:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        user_id = body.get("user_id")
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_place = Place(**body)
        new_place.city_id = city.id
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    all_places = []
    for plc in city.places:
        all_places.append(plc.to_dict())
    return jsonify(all_places)


@app_views.route(r4, methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def place_by_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
                setattr(place, k, v)
                # body[k] = v
        storage.save()
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
    return jsonify(place.to_dict())
