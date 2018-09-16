from flask import request
from flask_restful import Resource, reqparse
from models.user import User

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		required=True,
		type=str,
		help="Username required"
	)
	parser.add_argument('password',
		required=True,
		type=str,
		help="Password required"
	)

	def post(self):
		payload = self.parser.parse_args()
		username = payload['username']
		
		if User.find_by_username(username):
			return {"message": f"User with username '{username}' already exists"}, 400

		user = User(**payload)

		user.save_to_db()
		return {"message": f"User '{username}' created successfully"}, 201

class UserList(Resource):
	def get(self):
		users = User.query.all()
		return {"users": [user.json() for user in users]}, 200