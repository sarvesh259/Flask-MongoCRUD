from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import jsonify, request

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"

mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def add_user():
    _json = request.json
    bid = _json['id']
    _name = _json['name']
    _email = _json['email']
    _pwd = _json['pwd']

    if bid and _name and _email and _pwd and request.method == 'POST':
        existing_user = mongo.db.users.data.find_one({'_id': bid})
        if existing_user:
            return jsonify({'error': 'User with _id already exists'}), 400
        mongo.db.users.data.insert_one(
            {'_id': bid, 'name': _name, 'email': _email, 'pwd': _pwd})
        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp
    else:
        return jsonify({'error': 'Wrong Input, kindly recheck'}), 404


@app.route('/users')
def users():
    users = mongo.db.users.data.find()
    resp = dumps(users)
    return resp


@app.route('/users/<id>')
def find_one(id):
    one = mongo.db.users.data.find_one({'_id': id})
    if one:
        resp = dumps(one)
        return resp
    else:
        return jsonify({'error': 'Wrong Id, or Id doesn\'t exist'}), 404


@app.route('/users/<id>', methods=['DELETE'])
def delete_one(id):
    if (mongo.db.users.data.find_one({'_id': id})):
        mongo.db.users.data.delete_one({'_id': id})
        resp = jsonify("User deleted successfully")
        resp.status_code = 200
        return resp
    else:
        return jsonify({'error': 'Wrong Id, or Id doesn\'t exist'}), 404


@app.route('/users/<id>', methods=['PUT'])
def update_one(id):
    if (mongo.db.users.data.find_one({'_id': id})):
        _json = request.json
        bid = _json['_id']
        _name = _json['name']
        _email = _json['email']
        _pwd = _json['pwd']
        if bid and _name and _email and _pwd:
            mongo.db.users.data.update_one(
                {'_id': id}, {'$set': {'_id': bid, 'name': _name, 'email': _email, 'pwd': _pwd}})
            resp = jsonify("User Updated successfully")
            resp.status_code = 200
            return resp
        else:
            return jsonify({'error': 'Wrong Input, kindly recheck'}), 404
    else:
        return jsonify({'error': 'Wrong Id, or Id doesn\'t exist'}), 404


if __name__ == "__main__":
    app.run(debug=True)
