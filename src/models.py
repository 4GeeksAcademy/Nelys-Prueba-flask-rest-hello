from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.name,
            # do not serialize the password, its a security breach
        }
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    
    
  
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            
        }
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            
        }
class Favorites_Planets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets_relationship = db.relationship(Planets)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship(User)
    def __repr__(self):
        return '<Favorites_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id,
        } 
class Favorites_People(db.Model):
    __tablename__='favorites_people'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people_relationship = db.relationship(People)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship(User)

    def __repr__(self):
        return '<Favorites_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id,
        }