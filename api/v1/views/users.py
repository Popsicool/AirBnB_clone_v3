#!/usr/bin/python3
"""User module """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def users():
    """ get all users or create a new user"""
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "email" not in body:
            return make_response(jsonify({"error": "Missing email"}), 400)
        if "password" not in body:
            return make_response(jsonify({"error": "Missing password"}), 400)
        new_user = User(**body)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    all_users = storage.all("User")
    users_all = []
    for k, v in all_users.items():
        users_all.append(v.to_dict())
    return jsonify(users_all)


@app_views.route("users/<user_id>", methods=["GET", "DELETE", "PUT"])
def user(user_id):
    """update, delete or read a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'email', 'created_at', 'updated']:
                setattr(user, k, v)
                # body[k] = v
        storage.save()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})
    return jsonify(user.to_dict())
