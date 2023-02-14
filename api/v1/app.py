#!/usr/bin/python3
"""Where the app is created"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(self):
    """remove sqlAlchemy session"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """404 handling"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """run the app if its from main and not imported"""
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=int(port), threaded=True)
