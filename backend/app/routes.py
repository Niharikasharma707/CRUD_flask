from flask import request, jsonify
from app import app, db
from app.models import Item

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id}), 201


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])



@app.route('/items/<int:id>', methods=['PUT']) 
#update route
def update_item(id):
    data = request.json
    item = Item.query.get_or_404(id)
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})


@app.route('/items/<int:id>', methods=['DELETE'])
#delete route
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200


@app.route('/swagger.yaml')
def swagger_yaml():
    return send_from_directory(directory='.', path='swagger.yaml')


# update and delete api still left 

