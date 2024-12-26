from flask import Flask
from flask_restx import Api, Resource, fields
from app import db
from app.models import Item

app = Flask(__name__)
api = Api(app, version='1.0', title='Flask CRUD API',
          description='A simple CRUD API')

# Define the model for Swagger documentation
item_model = api.model('Item', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an item'),
    'name': fields.String(required=True, description='The name of the item'),
    'description': fields.String(required=True, description='The description of the item')
})

# Define the namespace
ns = api.namespace('items', description='Items operations')

@ns.route('/')
class ItemList(Resource):
    '''Shows a list of all items, and lets you POST to add new items'''
    @ns.doc('list_items')
    @ns.marshal_list_with(item_model)
    def get(self):
        '''List all items'''
        items = Item.query.all()
        return items

    @ns.doc('create_item')
    @ns.expect(item_model)
    @ns.marshal_with(item_model, code=201)
    def post(self):
        '''Create a new item'''
        data = api.payload
        new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201

@ns.route('/<int:id>')
@ns.response(404, 'Item not found')
@ns.param('id', 'The item identifier')
class ItemResource(Resource):
    '''Show a single item item and lets you delete them'''
    @ns.doc('get_item')
    @ns.marshal_with(item_model)
    def get(self, id):
        '''Fetch an item given its identifier'''
        item = Item.query.get_or_404(id)
        return item

    @ns.doc('delete_item')
    @ns.response(204, 'Item deleted')
    def delete(self, id):
        '''Delete an item given its identifier'''
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return '', 204

    @ns.expect(item_model)
    @ns.marshal_with(item_model)
    def put(self, id):
        '''Update an item given its identifier'''
        item = Item.query.get_or_404(id)
        data = api.payload
        item.name = data['name']
        item.description = data['description']
        db.session.commit()
        return item
