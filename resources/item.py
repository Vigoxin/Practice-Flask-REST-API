from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import Item

class ItemResource(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="Every item must have a price"
	)

	def get(self, name):
		item = Item.find_by_name(name)
		if item:
			return {"item": item.json()}
		return {"message": f"Item with name '{name}' not found"}, 404

	def post(self, name):
		if Item.find_by_name(name):
			return {"message": f"Item with name '{name}' already exists"}, 400

		payload = self.parser.parse_args()
		item = Item(name, payload['price'])
		try:
			item.save_to_db()
		except:
			return {"message": "Sorry, there was an error adding the item to the database"}, 500
		return {"item added": item.json()}, 201

	def put(self, name):
		item = Item.find_by_name(name)
		payload = self.parser.parse_args()
		
		if item:
			item.price = payload['price']
			message_key = 'item updated'
		else:
			item = Item(name, payload['price'])
			message_key = 'item added'

		item.save_to_db()
		return {message_key: item.json()}, 201 if message_key == 'item added' else 200

	@jwt_required()
	def delete(self, name):
		item = Item.find_by_name(name)
		if item:
			try:
				item.delete_from_db()
				return {"item deleted": item.json()}, 200
			except:
				return {"message": "Sorry, there was an error deleting the item from the database"}, 500

		return {"message": f"Item with name '{name}' not found"}, 404

class ItemListResource(Resource):
	def get(self):
		items = Item.query.all()
		return {"items": [item.json() for item in items]}, 200

	@jwt_required()
	def delete(self):
		items = Item.query.all()
		for item in items:
			item.delete_from_db()
		return {"message": "All items deleted"}

