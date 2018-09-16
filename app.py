from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required

from resources.item import ItemResource, ItemListResource
from resources.user import UserRegister, UserList
from security import authenticate, identity

from db import db

# Initialising app and app config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asdfasdfasdf'

# Initialising flask-restful api
api = Api(app)

# Creating tables
@app.before_first_request
def create_tables():
	db.create_all()

# Adding JWT
jwt = JWT(app, authenticate, identity)

# Adding resources to api as part of flask-restful
api.add_resource(ItemResource, '/item/<name>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
# api.add_resource(UserDelete, '/user')


if __name__ == '__main__':
	db.init_app(app)
	app.run(port=5002, debug=True)