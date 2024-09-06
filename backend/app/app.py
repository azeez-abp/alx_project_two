#!/usr/bin/python3
""" Flask Application """
from os import environ, makedirs, path

from dotenv import load_dotenv
from flasgger import Swagger  # type: ignore
from flask import Flask, jsonify, make_response, send_from_directory  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_restful import Api, Resource  # type: ignore
from v1 import token_route
from v1.users import users_route

load_dotenv()
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

app.register_blueprint(users_route)
app.register_blueprint(token_route)

"""parser = reqparse.RequestParser()"""

UPLOAD_FOLDER = path.join(path.dirname(path.abspath(__file__)), "uploads")
if not path.exists(UPLOAD_FOLDER):
    makedirs(UPLOAD_FOLDER)


@app.teardown_appcontext
def close_db(error):
    """Close Storage"""
    pass
    """storage.close() """


@app.errorhandler(404)
def not_found(error):
    """404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config["SWAGGER"] = {"title": "AirBnB clone Restful API", "uiversion": 3}

app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/uploads/<filename>")
def download_file(filename):
    print(filename)
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


Swagger(app)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        """
        A simple test API
        This ednpoint does nothing
        Only returs "test"

        """
        return {"hello": "world"}


class GetFile(Resource):
    def get(self, filename):
        print(filename)
        return send_from_directory(UPLOAD_FOLDER, filename)


api.add_resource(HelloWorld, "/")
api.add_resource(GetFile, "/uploads/<filename>")

if __name__ == "__main__":
    """Main Function"""
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")
    if not host:
        host = "127.0.0.1"
    if not port:
        port = "9393"
    app.run(host=host, port=int(port), threaded=True, debug=True)
