import random

# contains some utility functions for getting information about the board / potential moves

def is_same_space(space1, space2):
    return (space1['x'] == space2['x'] and space1['y'] == space2['y'])

def get_head(you):
    return you['body'][0]

def convert_move_to_new_head(cur_head, move):
    if move == 'up':
        return {'x': cur_head['x'], 'y': cur_head['y'] - 1}
    elif move == 'down':
        return {'x': cur_head['x'], 'y': cur_head['y'] + 1}
    elif move == 'right':
        return {'x': cur_head['x'] + 1, 'y': cur_head['y']}
    elif move == 'left':
        return {'x': cur_head['x'] - 1, 'y': cur_head['y']}


def is_snake(move, data):
    board = data['board']
    snakes = board['snakes']
    me = data['you']

    cur_head = me['body'][0]
    print('Turn %d, head is at: %d, %d' % (data['turn'], cur_head['x'], cur_head['y']))
    new_head = convert_move_to_new_head(cur_head, move)

    for snake in snakes:
        for square in snake['body']:
            if is_same_space(new_head, square):
                return True

    return False

def get_health(you):
    return you['health']
    
def find_food(board):
    return []

def get_direction_to_point(starting_point, goal_point):
    return 'UP'

def get_direction_to_open_space(starting_point):
    return 'UP'

def is_wall(move, data):
    board = data['board']
    
    width = board['width']
    height = board['height']
    me = data['you']


    cur_head = me['body'][0]
    new_head = convert_move_to_new_head(cur_head, move)

    if new_head['x'] == -1 or new_head['x'] == width or new_head['y'] == -1 or new_head['y'] == height:
        return True
    
    return False


def find_safe_move(data):
    directions = ['up', 'down', 'right', 'left']

    while len(directions) > 0:
        d = random.choice(directions)
        if not is_wall(d, data) and not is_snake(d, data):
            return d
        directions.remove(d)
    
    return 'up'
