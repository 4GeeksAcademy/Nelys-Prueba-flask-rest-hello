"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites_People, Favorites_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Metodos de User
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()  
    user_list = list(map(lambda user: user.serialize(), users))
    return jsonify(user_list), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg':'User not found'}), 400
    else:
        return jsonify({'msg':'ok','inf':user.serialize()})
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent = True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Debes enviar un nombre en el body'}), 400
    
    new_user = User()
    new_user.name = body['name']
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'ok'}),200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'El usuario de id:{} no existe'.format(user_id)})
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' in body:
        user.name = body['name']
    if 'email' in body:
        user.email = body['email']
    if 'password' in body:
        user.password = body['password']
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('El usuario con id {} no existe'.format(user_id), status_code=400)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
