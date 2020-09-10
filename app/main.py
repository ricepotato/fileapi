# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.resources.files import Files

app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)
api.add_resource(
    Files, "/files/<path:path>", resource_class_kwargs={}, endpoint="files",
)


@app.route("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
