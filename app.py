from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import Register, UserResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hadgznxasjghaygbnasn12986365gi=2t21y@$5mnzvxhgf"
api = Api(app)

@app.before_first_request
def create_db_tables():
    db.create_all()

app.config['JWT_AUTH_URL_RULE'] = '/login/'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify({
#         'message': error.description,
#         'code': error.status_code
#     }), error.status_code


api.add_resource(Item, "/items/<string:name>/")
api.add_resource(ItemList, "/items/")

api.add_resource(Register, "/register/")
api.add_resource(UserResource, "/me/")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)