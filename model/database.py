from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##### Model classes #####


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String)
    full_name = db.Column(db.String)
    choice_of_kart = db.Column(db.Boolean)
    allows_customisation = db.Column(db.Boolean)
    cup_length = db.Column(db.Integer)


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

    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    track = db.relationship('Track', backref=db.backref('times', lazy='dynamic'))

    character = db.Column(db.String)
    kart_body = db.Column(db.String)
    kart_wheels = db.Column(db.String)
    kart_glider = db.Column(db.String)

    proof_url = db.Column(db.String)

    def __repr__(self):
        minutes = int(self.milliseconds / (1000 * 60))
        leftover_seconds = self.milliseconds - (minutes * (1000 * 60))
        seconds = int(leftover_seconds / 1000)
        leftover_milliseconds = leftover_seconds - (seconds * 1000)

        if seconds < 10:
            seconds_str = "0{}".format(seconds)
        else:
            seconds_str = str(seconds)

        if leftover_milliseconds < 10:
            milliseconds_str = "00{}".format(leftover_milliseconds)
        elif leftover_milliseconds < 100:
            milliseconds_str = "0{}".format(leftover_milliseconds)
        else:
            milliseconds_str = str(leftover_milliseconds)

        return "{0}:{1}.{2}".format(minutes, seconds_str, milliseconds_str)


    def __lt__(self, other):
        return (self.milliseconds < other.milliseconds)


    def __le__(self, other):
        return (self < other) or (self == other)


    def __gt__(self, other):
        return not (self <= other)


    def __ge__(self, other):
        return not (self < other)


    def __eq__(self, other):
        return (self.milliseconds == other.milliseconds)


    def __ne__(self, other):
        return not (self == other)


    def __sub__(self, other):
        return self.milliseconds - other.milliseconds


##### Interaction functions #####


def add_object(game):
    db.session.add(game)
    commit_changes()


def count(_class):
    objects = _class.query.all()
    return len(objects)


def game_already_exists(short_name):
    game = Game.query.filter_by(short_name=short_name).first()
    return (game is not None)


def get(_class, obj_id):
    obj = _class.query.filter_by(id=obj_id).first()
    return obj


def get_all(_class):
    objects = _class.query.all()
    objects = sorted(objects, key=lambda obj: obj.id)
    return objects


def get_game_by_short_name(short_name):
    game = Game.query.filter_by(short_name=short_name).first()
    return game


def get_track_time_for_person(track_id, person_id):
    return get(Track, track_id).times.filter_by(person_id=person_id).first()


def track_already_exists(name, game_id):
    track = Track.query.filter_by(name=name, game_id=game_id).first()
    return (track is not None)


def person_already_exists(name):
    person = Person.query.filter_by(name=name).first()
    return (person is not None)


def replace(old_obj, new_obj):
    if old_obj is not None:
        db.session.delete(old_obj)
    db.session.add(new_obj)
    commit_changes()


##### High level functions #####


def create_tables():
    db.create_all()


def commit_changes():
    db.session.commit()

