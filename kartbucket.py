import csv
import os
import newrelic.agent
from flask import Flask, url_for, render_template, request, jsonify, redirect
from model import database
from utils import utils

##### Config #####

newrelic.agent.initialize('newrelic.ini')

app = Flask(__name__)
app.config["SECRET_KEY"] = "d47d2b74ff64e5a6ae5aedd4edebeaf1"

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError as error:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost:5432"

database.db.init_app(app)

options = {}

# Horrible flask-ness to allow access to the database from outside of
# a route
with app.app_context():
    try:
        options['all_games'] = database.get_all(database.Game)[::-1]
    except Exception as error:
        database.create_tables()
        options['all_games'] = database.get_all(database.Game)[::-1]
        

##### Pages #####


@app.route('/')
def index():
    options['title'] = "Kartbucket"
    options['game'] = database.get(database.Game, database.count(database.Game))
    options['active_page'] = options['game'].short_name

    return redirect(url_for('game_name', game_name=options['game'].short_name))


@app.route('/game/<game_name>/')
def game_name(game_name):
    game = database.get_game_by_short_name(game_name)

    options['active_page'] = game_name
    options['game'] = game
    options['title'] = "{} - Kartbucket".format(game.full_name)

    options['tracks'] = sorted(game.tracks.all(), key=lambda track: track.id)
    options['cups'] = len(options['tracks']) / game.cup_length
    options['people'] = database.get_all(database.Person)

    return render_template('game.html', options=options)


@app.route('/game/<int:game_id>/')
def game_id(game_id):
    game = database.get(database.Game, game_id)
    return redirect(url_for('game_name', game_name=game.short_name))


@app.route('/setup/')
def setup():
    database.create_tables()

    with open('static/games.csv') as f:
        current_row = 0
        reader = csv.reader(f)
        for row in reader:
            if current_row > 0:
                game = database.Game()
                game.short_name = row[1]
                game.full_name = row[2]
                game.choice_of_kart = (row[3] == '1')
                game.allows_customisation = (row[4] == '1')
                game.cup_length = int(row[5])

                if not database.game_already_exists(game.short_name):
                    database.add_object(game)

            current_row += 1

    with open('static/tracks.csv') as f:
        current_row = 0
        reader = csv.reader(f)
        for row in reader:
            if current_row > 0:
                track = database.Track()
                track.name = row[1]
                track.game_id = row[2]
                
                if not database.track_already_exists(track.name, track.game_id):
                    database.add_object(track)

            current_row += 1


    with open('static/people.csv') as f:
        current_row = 0
        reader = csv.reader(f)
        for row in reader:
            if current_row > 0:
                person = database.Person()
                person.name = row[1]

                if not database.person_already_exists(person.name):
                    database.add_object(person)

            current_row += 1

    return "Setup complete!"


##### API Endpoints #####





##### Template Filters #####





##### Main #####

if (__name__ == "__main__"):
    app.run(debug=True)
