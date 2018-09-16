import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db import db

class Item(db.Model):

	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))

	def __init__(self, name, price):
		self.__dict__.update(locals())
		del self.self

	def json(self):
		return {'name': self.name, 'price': self.price, 'id': self.id}
		# j = self.__dict__.copy()
		j = vars(self).copy()
		j.pop('_sa_instance_state', None)
		return j

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	def save_to_db(self):
		# Adds (if there doesn't exist) as well as updates (if there exists) an item with the same id
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

if __name__ == '__main__':
	i = Item('asdf', 12)
	print(i.json())