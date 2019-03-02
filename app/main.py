import json
import os
import random
import bottle
from util import *
import util
from random import shuffle


from api import ping_response, start_response, move_response, end_response
import util


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    print(data)	

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    LOW_HEALTH_THRESHOLD = 50

    you = data['you']
    board = data['board']

    directions = ['up', 'down', 'left', 'right']
    direction = None
    move_history = get_move_history()
    last_move = None

    if False:
        # go to find food
        find_food = util.find_food(data)
        sort_food = util.sort_food(data, find_food)
    else:
        # move towards an open space

        quadrants = get_adjacent_quadrant_densities(get_head(you), data)

        if len(move_history) > 0:
            last_move = move_history[0]
        for quadrant in quadrants:
            pos_moves = get_quadrant_moves(quadrant)
            shuffle(pos_moves)
            # print("Quadrant %s, density %f" % (quadrant["id"], quadrant["density"]))
            if last_move in pos_moves:
                if is_move_safe(last_move, data):
                    direction = last_move
                    break
            else:
                for move in pos_moves:
                    if is_move_safe(move, data):
                        direction = move
                        break
                    
            if direction is not None:
                break
        if direction is None:
            direction = util.find_safe_move(data)

    print(direction)
    add_move_to_history(direction)
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', False)
    )