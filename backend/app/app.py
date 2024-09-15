#!/usr/bin/env python
""" Flask Application """
from datetime import timedelta
from os import environ, getenv, makedirs, path

from dotenv import load_dotenv
from flasgger import Swagger  # type: ignore
from flask import jsonify  # type: ignore
from flask import Flask, make_response, send_from_directory
from flask_cors import CORS  # type: ignore
from flask_restful import Api, Resource  # type: ignore
from libs.upload_file import upload_from_multipart  # type: ignore
from resouces import resource_product_revenue_route  # type: ignore
from v1 import token_route  # type: ignore
from v1.users import users_route  # type: ignore
# from v1.products import products_route

load_dotenv()
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

app.register_blueprint(users_route)
app.register_blueprint(token_route)
app.register_blueprint(resource_product_revenue_route)
# app.register_blueprint(products_route)

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
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/test_upload", methods=["POST"])
def handel_upload():
    path = upload_from_multipart()
    print(path[1], "tyt")
    return jsonify({"a": str(path)})


Swagger(app)
api = Api(app)

# App configurations
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    minutes=15
)  # Access token expires in 15 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    days=30
)  # Refresh token expires in 30 days

# Flask-Session config for storing refresh tokens in cookies
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_NAME"] = getenv("FARM_APP")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

# Initialize extensions


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
