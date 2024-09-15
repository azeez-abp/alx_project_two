from flask import Flask  # type:ignore
from flask_restful import Api, Resource, request  # type:ignore

app = Flask(__name__)
api = Api(app)


class MethodNotInResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        if request.method not in self.methods:
            return {"error": f"Method {request.method} not allowed"}, 405
        return super().dispatch_request(*args, **kwargs)
