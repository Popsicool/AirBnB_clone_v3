#!/usr/bin/python3
"""cities module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("states/<string:state_id>/cities", methods=["GET", "POST"])
def states_cities(state_id):
    """states city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_city = City(**body)
        new_city.state_id = state.id
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    all_cities = []
    for cty in state.cities:
        all_cities.append(cty.to_dict())
    return jsonify(all_cities)


@app_views.route("cities/<city_id>", methods=["GET", "PUT", "DELETE"])
def city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'created_at', 'updated']:
                setattr(city, k, v)
                # body[k] = v
        storage.save()
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
    return jsonify(city.to_dict())
