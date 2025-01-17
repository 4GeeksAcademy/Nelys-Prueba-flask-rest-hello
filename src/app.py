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
    if 'email' not in body:
        return jsonify({'msg': 'Debes enviar un email en el body'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'Debes enviar un nombre en el body'}), 400
    
    new_user = User(name=body['name'], email=body['email'], password=body['password'],is_active=True)
    
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

#Metodos de Tabla Planets

@app.route('/planets', methods=['GET'])
def get_planet():
    planets = Planets.query.all()  
    planets_list = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(planets_list), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 400
    else:
        return jsonify({'msg': 'ok', 'inf': planet.serialize()})


@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json(silent=True)
    print(body)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Debes enviar un nombre en el body'}), 400
    
    new_planet = Planets()
    new_planet.name = body['name']
    new_planet.diameter = body['diameter']
    new_planet.rotation_period = body['rotation_period']
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'msg': 'ok'}),200
    
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planets(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'El planeta de id:{} no existe'.format(planet_id)})
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' in body:
        planet.name = body['name']
    if 'diameter' in body:
        planet.diameter = body['diameter']
    if 'rotation_period' in body:
        planet.rotation_period = body['rotation_period']
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException('El planeta con id {} no existe'.format(planet_id), status_code=400)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

# Tabla People
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()  
    people_list = list(map(lambda people: people.serialize(), people))
    return jsonify(people_list), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id)
    if people is None:
        return jsonify({'msg': 'People not found'}), 400
    else:
        return jsonify({'msg': 'ok', 'inf': people.serialize()})
    
@app.route('/people', methods=['POST'])
def create_people():
    body = request.get_json(silent=True)
    print(body)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Debes enviar un nombre en el body'}), 400
    
    new_people = People()
    new_people.name = body['name']
    new_people.height = body['height']
    new_people.mass = body['mass']
    new_people.hair_color = body['hair_color']
    db.session.add(new_people)
    db.session.commit()

    return jsonify({'msg': 'ok'}),200

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        return jsonify({'msg': 'El personaje de id:{} no existe'.format(people_id)})
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' in body:
        people.name = body['name']
    if 'height' in body:
        people.height = body['height']
    if 'mass' in body:
        people.mass = body['mass']
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        raise APIException('El personaje con id {} no existe'.format(people_id), status_code=400)
    db.session.delete(people)
    db.session.commit()
    return jsonify({'msg':'ok'}), 200
    
# Tablas favoritos  El resultado que me devuelve es en numero y supongo q debe ser en string
@app.route('/user/<int:id_user>/favorites', methods=['GET'])
def get_favorites_de_user_planet(id_user):
    favorites_planet = Favorites_Planets.query.filter_by(user_id = id_user)
    favorites_people = Favorites_People.query.filter_by(user_id = id_user)
    favorites_list1 = list(map(lambda favorite: favorite.serialize(), favorites_planet))
    favorites_list2 = list(map(lambda favorite: favorite.serialize(), favorites_people))
    favorites_list1.extend(favorites_list2)
    return jsonify({'msg': 'ok', 'inf': favorites_list1})

@app.route('/favorites_planets/<int:user_id>', methods=['POST'])
def create_favorites_planets(user_id):
    body = request.get_json(silent=True)
    print(body)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    
    new_favorite_planet = Favorites_Planets()
    new_favorite_planet.planet_id = body['planet_id']
    new_favorite_planet.user_id = user_id
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({'msg': 'ok'}),200
@app.route('/favorites_planets/<int:favorite_planets_id>', methods=['DELETE'])
def delete_favorites_planets(favorite_planets_id):
    favorites_planets = Favorites_Planets.query.get(favorite_planets_id)
    if favorite_planets_id is None:
        raise APIException('La relacion de favoritos planetas con id {} no existe'.format(favorite_planets_id), status_code=400)
    db.session.delete(favorites_planets)
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

@app.route('/favorites_people/<int:user_id>', methods=['POST'])
def create_favorites_people(user_id):
    body = request.get_json(silent=True)
    print(body)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    
    new_favorite_people = Favorites_People()
    new_favorite_people.people_id = body['people_id']
    new_favorite_people.user_id = body['user_id']
    db.session.add(new_favorite_people)
    db.session.commit()

    return jsonify({'msg': 'ok'}),200

@app.route('/favorites_people/<int:favorite_people_id>', methods=['DELETE'])
def delete_favorites_people(favorite_people_id):
    favorites_people = Favorites_People.query.get(favorite_people_id)
    if favorite_people_id is None:
        raise APIException('La relacion de favoritos planetas con id {} no existe'.format(favorite_people_id), status_code=400)
    db.session.delete(favorites_people)
    db.session.commit()
    return jsonify({'msg':'ok'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
