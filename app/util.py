import random

# contains some utility functions for getting information about the board / potential moves


def get_quadrant_size(board):
    if board.width < 10:
        return 2
    if board.width < 15:
        return 3
    if board.width < 20:
        return 4
    else:
        return 5

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

    if new_head['x'] <= -1 or new_head['x'] >= width or new_head['y'] <= -1 or new_head['y'] => height:
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

def get_adjacent_quadrant_densities(starting_point, data):
    board = data['board']
    # returns the adjacent quadrants
    # if a wall if in a quadrant, it is not returned as a viable quadrant
    quad_size = get_quadrant_size(board)
    # define a quadrant by it's top left and bottom right corners
    top_left_quad = { 
        top_left: { 'x': starting_point['x'] - quad_size, 'y': starting_point['y'] - quad_size },
        bottom_right: { starting_point }
    }
    top_right_quad = {
        top_left: { 'x': starting_point['x'], 'y': starting_point['y'] - quad_size },
        bottom_right: { 'x': starting_point[x] + quad_size, starting_point['y'] }
    }
    bottom_left_quad = { 
        top_left: { 'x': starting_point['x'] - quad_size, 'y': starting_point['y'] },
        bottom_right: { 'x': starting_point['x'], starting_point['y'] + quad_size }
    }
    bottom_right_quad = { 
        top_left: { 'x': starting_point['x'], 'y': starting_point['y'] },
        bottom_right: { 'x': starting_point['x'] + quad_size, 'y': starting_point['y'] + quad_size}
    }

    quad_densities = {
        "top_left": get_quadrant_density(top_left, quad_size, data),
        "top_right": get_quadrant_density(top_right, quad_size, data),
        "bottom_left": get_quadrant_density(bottom_left, quad_size, data),
        "bottom_right": get_quadrant_density(bottom_right, quad_size, data),
    }

    return quad_densities
    

def get_quadrant_density(quadrant, quad_size, data):
    num_quad_squares = quad_size * quad_size
    full_squares = 0
    top_left = quadrant['top_left']
    bottom_right = quadrant['bottom_right']
    for x in range(top_left['x'], bottom_right['x']):
        for y in range(top_left['y'], bottom_right['y']):
            point = {'x': x,'y': y}
            if is_snake(point, data) or is_wall(point, data):
                full_squares += 1
    return full_squares / num_quad_squares
                


