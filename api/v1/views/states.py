""" state module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route("/states")
def states():
    all_states = storage.all("State")
    states_all = []
    for k, v in all_states.items():
        states_all.append(v.to_dict())
    return jsonify(states_all)

@app_views.route("/states/<state_id>", methods=["GET", "DELETE"])
def state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})
    return jsonify(state.to_dict())
    # all_states = storage.all("State")
    # for k, v in all_states.items():
    #     if k.split(".")[1] == state_id:
    #         return jsonify(v.to_dict())
