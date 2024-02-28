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
from models import db, User, Planets, Characters, Favorites
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

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    return jsonify(user.serialize()), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    request_body = request.get_json()
    user_id = request_body.get("user_id", None)
    if user_id is None:
        raise APIException("User ID is required", status_code=400)
    favorites = Favorites.query.filter_by(user_id=user_id)
    favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify({
        "user_id": user_id,
        "favorites": favorites
    }), 200

@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    request_body = request.get_json()
    user_id = request_body.get("user_id", None)
    if user_id is None:
        raise APIException("User ID is required", status_code=400)
    favorite = Favorites(
        user_id=user_id,
        character_id=character_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
