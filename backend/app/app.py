#!/usr/bin/env python
""" Flask Application """
from datetime import timedelta
from os import environ, getenv, makedirs, path

from dotenv import load_dotenv
from flasgger import Swagger  # type: ignore
from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS  # type: ignore
from flask_restful import Api, Resource  # type: ignore
from resouces import resource_product_revenue_route  # type: ignore
from v1 import token_route  # type: ignore
from v1.users import users_route  # type: ignore

from app.libs.upload_file import upload_from_multipart  # type: ignore

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


def create_app(testing: bool = False):
    """Create and configure the Flask app."""

    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.config["UPLOAD_FOLDER"] = "uploads"

    if testing:
        app.config["TESTING"] = True

    app.register_blueprint(users_route)
    app.register_blueprint(token_route)
    app.register_blueprint(resource_product_revenue_route)

    # File upload setup
    UPLOAD_FOLDER = path.join(path.dirname(path.abspath(__file__)), "uploads")
    if not path.exists(UPLOAD_FOLDER):
        makedirs(UPLOAD_FOLDER)

    # Swagger setup
    Swagger(app)
    api = Api(app)

    # App configurations
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # Flask-Session config
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_COOKIE_NAME"] = getenv("FARM_APP")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

    # Error handler
    @app.errorhandler(404)
    def not_found(error):
        """404 Error Handler"""
        return make_response(jsonify({"error": "Not found"}), 404)

    # File download route
    @app.route("/uploads/<filename>")
    def download_file(filename):
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )

    @app.route("/test_upload", methods=["POST"])
    def handel_upload():
        path = upload_from_multipart()
        return jsonify({"path": str(path)})

    # API Resources
    class HelloWorld(Resource):
        def get(self):
            """A simple test API"""
            return {"hello": "world"}

    class GetFile(Resource):
        def get(self, filename):
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    api.add_resource(HelloWorld, "/")
    api.add_resource(GetFile, "/uploads/<filename>")

    return app


if __name__ == "__main__":
    """Main Function"""
    host = environ.get("HBNB_API_HOST", "127.0.0.1")
    port = environ.get("HBNB_API_PORT", "9393")
    app = create_app()
    app.run(host=host, port=int(port), threaded=True, debug=True)
