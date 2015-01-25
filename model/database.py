from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##### Model classes #####


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String)
    full_name = db.Column(db.String)
    choice_of_kart = db.Column(db.Boolean)
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
    milliseconds = db.Column(db.Integer)
    split1_mils = db.Column(db.Integer)
    split2_mils = db.Column(db.Integer)
    split3_mils = db.Column(db.Integer)  

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref=db.backref('times', lazy='dynamic'))

    character = db.Column(db.String)
    kart_body = db.Column(db.String)
    kart_wheels = db.Column(db.String)
    kart_glider = db.Column(db.String)

    proof_url = db.Column(db.String)

    def __lt__(self, other):
        if self.minutes < other.minutes:
            return True

        elif (self.minutes == other.minutes) and (self.seconds < other.seconds):
            return True

        elif (self.minutes == other.minutes) and (self.seconds == other.seconds) and (self.milliseconds < other.milliseconds):
            return True

        else:
            return False


    def __le__(self, other):
        return (self < other) or (self == other)


    def __gt__(self, other):
        return not (self <= other)


    def __ge__(self, other):
        return not (self < other)


    def __eq__(self, other):
        return (self.minutes == other.minutes) and (self.seconds == other.seconds) and (self.milliseconds == other.milliseconds)


    def __ne__(self, other):
        return not (self == other)


##### Interaction functions #####


def add_object(game):
    db.session.add(game)
    commit_changes()


def game_already_exists(short_name):
    game = Game.query.filter_by(short_name=short_name).first()
    return (game is not None)


def track_already_exists(name, game_id):
    track = Track.query.filter_by(name=name, game_id=game_id).first()
    return (track is not None)


def person_already_exists(name):
    person = Person.query.filter_by(name=name).first()
    return (person is not None)


##### High level functions #####


def create_tables():
    db.create_all()


def commit_changes():
    db.session.commit()

