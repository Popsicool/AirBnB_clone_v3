#!/usr/bin/python3
"""Review module"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route("places/<place_id>/reviews", methods=["GET", "POST"])
def places_review(place_id):
    """Places review"""
    place = storage.get(Place, place_id)
    if not place:
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
        if "text" not in body:
            return make_response(jsonify({"error": "Missing text"}), 400)
        new_review = Review(**body)
        new_review.place_id = place.id
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    all_reviews = []
    for rev in place.reviews:
        all_reviews.append(rev.to_dict())
    return jsonify(all_reviews)


@app_views.route("reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def review_by_id(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
                setattr(review, k, v)
                # body[k] = v
        storage.save()
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})
    return jsonify(review.to_dict())
