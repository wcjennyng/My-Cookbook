from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

IMAGE_URL = 'https://tinyurl.com/3dwtk22x'

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


#MODELS BELOW

class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    recipe = db.relationship('Recipes', backref='user', cascade='all, delete')
    favorites = db.relationship('Favorites', backref='user', cascade='all, delete')

    @property
    def full_name(self):
        """Full name of user"""
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, 
                   password=hashed_utf8, 
                   email=email, 
                   first_name=first_name, 
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        



class Recipes(db.Model):
    """Recipes"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime('%a, %d. %b %Y %I:%M%p'))
    favorite = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)


    def image(self):
        """Image for recipe or default image"""
        return self.photo_url or IMAGE_URL

class Favorites(db.Model):
    """Favorites"""

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

