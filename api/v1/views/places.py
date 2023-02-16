#!/usr/bin/python3
"""Place module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State

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
    """ place by id"""
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


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """place search"""
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if not body or not len(body) or (
                not body.get("states") and not body.get("cities")
                and not body.get("amenities")):
            all_places = storage.all("Place")
            plc_all = []
            for k, v in all_places.items():
                plc_all.append(v.to_dict())
            return jsonify(plc_all)
        response = []
        states = body.get("states")
        if states:
            all_states = []
            for id in states:
                all_states.append(storage.get(State, id))
            for st in all_states:
                if st:
                    for city in st.cities:
                        if city:
                            for place in city.places:
                                response.append(place)
        cities = body.get("cities")
        if cities:
            all_cities = []
            for id in cities:
                all_cities.append(storage.get(City, id))
            for cty in all_cities:
                if cty:
                    for place in cty.places:
                        if place not in response:
                            response.append(place)
        amenities = body.get("amenities")
        if amenities:
            if not response:
                all_places = storage.all("Place")
                for k, v in all_places.items():
                    amenities.append(v.to_dict())
            amenity_list = []
            for id in amenities:
                amenity_list.append(storage.get(Amenity, id))
            response = [place for place in response
                        if all([amen in place.amenities
                               for amen in amenities_list])]
        result = []
        for plc in response:
            plc_dic = plc.to_dict()
            plc_dic.pop('amenities', None)
            result.append(plc_dic)

        return jsonify(result)
