#!/usr/bin/python3
"""place amenity module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


ad1 = "/places/<place_id>/amenities"
ad2 = "places/<place_id>/amenities/<amenity_id>"


@app_views.route(ad1, strict_slashes=False)
def place_amen(place_id):
    """place amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_of_amenity = []
    for amenity in place.amenities:
        list_of_amenity.append(amenity.to_dict())

    return jsonify(list_of_amenity)


@app_views.route(ad2, methods=["DELETE", "POST"], strict_slashes=False)
def place_by_amen(place_id, amenity_id):
    """place and amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == "POST":
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
        storage.save()
        return (jsonify(amenity.to_dict(), 201))
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})
