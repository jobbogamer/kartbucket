from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##### Model classes #####


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    allows_customisation = db.Column(db.Boolean)


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('tracks', lazy='dynamic'))


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    minutes = db.Column(db.Integer)
    seconds = db.Column(db.Integer)
    milliseconds = db.Column(db.Integer)

    split1_mins = db.Column(db.Integer)
    split1_secs = db.Column(db.Integer)
    split1_mils = db.Column(db.Integer)

    split2_mins = db.Column(db.Integer)
    split2_secs = db.Column(db.Integer)
    split2_mils = db.Column(db.Integer)

    split3_mins = db.Column(db.Integer)
    split3_secs = db.Column(db.Integer)
    split3_mils = db.Column(db.Integer)  

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref=db.backref('times', lazy='dynamic'))

    character = db.Column(db.String)
    kart_body = db.Column(db.String)
    kart_wheels = db.Column(db.String)
    kart_glider = db.Column(db.String)

    proof_url = db.Column(db.String)


##### Interaction functions #####





##### High level functions #####


def create_tables():
    db.create_all()

