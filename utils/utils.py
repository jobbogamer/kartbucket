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


def api_add(args):
    track_id = int(args.get('track', ''))
    person_id = int(args.get('person', ''))
    time = args.get('time', '')
    split1 = args.get('split1', '')
    split2 = args.get('split2', '')
    split3 = args.get('split3', '')
    character = args.get('character', '???')
    kart = args.get('kart', '???')
    wheels = args.get('wheels', '???')
    glider = args.get('glider', '???')
    proof = args.get('proof', '???')

    result = {
        "success": False
    }

    milliseconds = time_str_to_milliseconds(time)
    if milliseconds is None:
        result['message'] = "The time was not entered in the correct XX:YY.ZZZ format."
        return result

    if len(split1) > 0 or len(split2) > 0 or len(split3) > 0:
        split1_mils = split_str_to_milliseconds(split1)
        split2_mils = split_str_to_milliseconds(split2)
        split3_mils = split_str_to_milliseconds(split3)

        total_mils = split1_mils + split2_mils + split3_mils
        if total_mils != milliseconds:
            result['message'] = "The split times do not add up to the total time."
            return result

    else:
        split1_mils = -1
        split2_mils = -1
        split3_mils = -1

    current_time = database.get_track_time_for_person(track_id, person_id)
    if (current_time is None) or milliseconds <= current_time.milliseconds:
        new_time = database.Time()
        new_time.track_id = track_id
        new_time.person_id = person_id
        new_time.milliseconds = milliseconds
        new_time.split1_mils = split1_mils
        new_time.split2_mils = split2_mils
        new_time.split3_mils = split3_mils
        new_time.character = character
        new_time.kart_body = kart
        new_time.kart_wheels = wheels
        new_time.kart_glider = glider
        new_time.proof_url = proof
        database.replace(current_time, new_time)

        result['success'] = True
        return result

    else:
        result['message'] = "You'll have to do better! Your current best time is {}.".format(current_time)
        return result


def api_time(args):
    track_id = int(args.get('track', ''))
    person_id = int(args.get('person', ''))

    result = {
        'success': False
    }

    time = database.get_track_time_for_person(track_id, person_id)
    track = database.get(database.Track, track_id)
    game = database.get(database.Game, track.game_id)

    if time is None:
        person = database.get(database.Person, person_id)
        result['message'] = "{0} hasn't set a time for {1}.".format(person.name, track.name)
        return result

    result['success'] = True
    result['time'] = str(time)
    result['split1'] = split_to_string(time.split1_mils)
    result['split2'] = split_to_string(time.split2_mils)
    result['split3'] = split_to_string(time.split3_mils)
    result['character'] = time.character or '???'
    result['proof_url'] = time.proof_url
    result['choice_of_kart'] = game.choice_of_kart
    result['allows_customisation'] = game.allows_customisation
    
    if game.allows_customisation:
        result['kart'] = time.kart_body or '???'
        result['wheels'] = time.kart_wheels or '???'
        result['glider'] = time.kart_glider or '???'
    elif game.choice_of_kart:
        result['kart'] = time.kart_body or '???'

    return result


def build_times_structure(game_id):
    game = database.get(database.Game, game_id)
    people = database.get_all(database.Person)
    tracks = game.tracks.all()

    struct = []

    for track in tracks:
        times = []
        stored_times = track.times.all()

        for person in people:
            found = False
            for time in stored_times:
                if time.person_id == person.id:
                    times.append(time)
                    found = True
                    break

            if not found:
                times.append(None)

        struct.append(times)

    return struct


def split_str_to_milliseconds(split_str):
    seconds_end = split_str.find('.')
    milliseconds_start = seconds_end + 1

    if seconds_end == -1:
        return -1

    try:
        seconds = float(split_str)
    except Exception as error:
        return -1

    return (seconds * 1000)


def split_to_string(milliseconds):
    if milliseconds == -1:
        return None

    seconds = int(milliseconds / 1000)
    leftover_milliseconds = milliseconds - (seconds * 1000)

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

    return "{0}.{1}".format(seconds_str, milliseconds_str)


def time_str_to_milliseconds(time_str):
    minutes_end = time_str.find(':')
    seconds_start = minutes_end + 1
    seconds_end = time_str.find('.', seconds_start)

    if minutes_end == -1 or seconds_end == -1:
        return None

    try:
        minutes = int(time_str[:minutes_end])
        seconds = float(time_str[seconds_start:])
    except Exception as error:
        return None

    return (seconds * 1000) + (minutes * 1000 * 60)

