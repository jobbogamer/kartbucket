from model import database


def splits_match_total(total_mins,  total_secs,  total_mils,
                       split1_mins, split1_secs, split1_mils,
                       split2_mins, split2_secs, split2_mils,
                       split3_mins, split3_secs, split3_mils):
    
    total  = total_mils  + (total_secs  * 1000) + (total_mins  * 60 * 1000)
    split1 = split1_mils + (split1_secs * 1000) + (split1_mins * 60 * 1000)
    split2 = split2_mils + (split2_secs * 1000) + (split2_mins * 60 * 1000)
    split3 = split3_mils + (split3_secs * 1000) + (split3_mins * 60 * 1000)

    return (total == (split1 + split2 + split3))


def build_times_structure(game_id):
    game = database.get(database.Game, game_id)
    people = database.get_all(database.Person)
    tracks = game.tracks.all()

    struct = {}

    for track in tracks:
        times = []
        stored_times = track.times.all()
        
        for person in people:
            for time in stored_times:
                found = False

                if time.person_id == person.id:
                    times.append(time)
                    found = True
                    break

                if not found:
                    times.append(None)

        struct[track.name] = times

    return struct
