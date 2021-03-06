import json
import os
import random
import bottle
# from app.api import *
# from app.util import *
from app.api import *
from app.util import *
from random import shuffle

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

    color = "#9D17B5"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    need_food_state = need_food(data)
    print("need food state is")
    print(need_food_state)
    print(data)
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    LOW_HEALTH_THRESHOLD = 70

    you = data['you']
    board = data['board']

    directions = ['up', 'down', 'left', 'right']
    direction = None
    move_history = get_move_history()
    last_move = None

    if need_food(data):
        pos_direction = get_food(data, get_head(you))

        if pos_direction['x_dir'] is not None:
            if is_move_safe(pos_direction['x_dir'], data):
                direction = pos_direction['x_dir']

        if pos_direction['y_dir'] is not None:
            if is_move_safe(pos_direction['y_dir'], data):
                direction = pos_direction['y_dir']
    
    if direction is None:
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
        direction = find_safe_move(data)

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