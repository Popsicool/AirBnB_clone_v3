#!/usr/bin/python3
""" state module """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


r8 = "/states/<state_id>"


@app_views.route("/states/", methods=["GET", "POST"], strict_slashes=False)
def states():
    """ get all states or create a new state"""
    if request.method == "POST":
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**body)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    all_states = storage.all("State")
    states_all = []
    for k, v in all_states.items():
        states_all.append(v.to_dict())
    return jsonify(states_all)


@app_views.route(r8, methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def state(state_id):
    """update, delete or read a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for k, v in body.items():
            if k not in ['id', 'created_at', 'updated']:
                setattr(state, k, v)
                # body[k] = v
        storage.save()
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})
    return jsonify(state.to_dict())
    # all_states = storage.all("State")
    # for k, v in all_states.items():
    #     if k.split(".")[1] == state_id:
    #         return jsonify(v.to_dict())
