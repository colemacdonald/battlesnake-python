import random
import math

from operator import itemgetter, attrgetter, methodcaller 
import pdb
import copy
from queue import Queue
import copy

MAX_MOVE_HISTORY = 100
move_history = []

def add_move_to_history(move):
    move_history.insert(0, move)
    if len(move_history) > MAX_MOVE_HISTORY:
        move_history.pop()

def get_move_history():
    global move_history
    return move_history
# contains some utility functions for getting information about the board / potential moves

def get_quadrant_size(board):
    if board['width'] < 10:
        return 4
    if board['width'] < 15:
        return 4
    if board['width'] < 20:
        return 5
    else:
        return 6


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
    snakes.append(me)

    cur_head = me['body'][0]
    new_head = convert_move_to_new_head(cur_head, move)

    return is_snake_space(new_head, board, snakes)

def is_snake_space(point, board, snakes):
    for snake in snakes:
        for square in snake['body']:
            if is_same_space(point, square):
                return True
                
        head = get_head(snake)
        if len(snake['body']) > len(board['you']['body']):
            for d in ['right', 'left', 'up', 'down']:
                if is_same_space(convert_move_to_new_head(head, d)):
                    return True

    return False
    
def find_walls(data):
    #the last available space before death is x number away
    #board size
    width = data['board']['width']
    height = data['board']['height']

    #where my head is 
    me = data['you']
    head = me['body'][0]

    #find dist to walls
    walls_dist = { 
        'up':head['y'],
        'down':height - head['y'] - 1,
        'left':head['x'],
        'right':width - head['x'] - 1
    }
    print(walls_dist)
    return walls_dist

def get_health(you):
    return you['health']
	
def cur_head(game):
    me = game['you']
    cur_head = me['body'][0]
    return cur_head	
	
def find_food(game):

    food_locations = game['board']['food']
    print(food_locations)
	
    return food_locations
	
def sort_food(game, food_locations):
    cur_head = game['you']['body'][0]
    for food in food_locations: 
        dist = abs(cur_head['x'] - food['x']) + abs(cur_head['y'] - food['y'])		
        food['dist'] = dist	
    return food_locations

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

    return is_wall_space(new_head, width, height)

def is_wall_space(point, board_width, board_height):
    if point['x'] <= -1 or point['x'] >= board_width or point['y'] <= -1 or point['y'] >= board_height:
        return True
    else:
        return False
    

def find_safe_move(data, epoch=1):
    directions = ['up', 'down', 'right', 'left']
    safe_directions = []

    # find safe directions
    for d in directions:
        if not is_wall(d, data) and not is_snake(d, data):
            safe_directions.append(d)    

    # check safe directions
    while len(safe_directions) > 0:
        d = random.choice(safe_directions)
        dead_end = is_dead_end(d, data, 10)
        if not is_wall(d, data) and not is_snake(d, data) and not dead_end:
            return d

        safe_directions.remove(d)
    
    return 'up'

def find_closest_food(data):
    me = data['you']
    health = me['health']
    food = find_food(data)
    sorted_food = sort_food(data, food)
    min_dist = 100
    i = 0
    index_min = 0
    for foods in sorted_food:
        print(foods['dist'])
        if foods['dist'] < min_dist:
            min_dist = foods['dist']
            index_min = i
        i = i+1

    closest_food = sorted_food[index_min]
    return closest_food

def need_food(data):
    me = data['you']
    health = me['health']
    closest_food = find_closest_food(data)

    distance_to_food = closest_food['x'] + closest_food['y']
    
    if health < distance_to_food:
        return True
    else:
         return False

def get_food(data, cur_pos):
    closest_food = find_closest_food(data)
    me = data['you']

    head = me['body'][0]

    pos_direction = { }
    
    x_dist = abs(cur_pos['x'] - closest_food['x'])
    y_dist = abs(cur_pos['y'] - closest_food['y'])

    if cur_pos['x'] == closest_food['x']:
        pos_direction['x_dir'] = None
    elif cur_pos['x'] > closest_food['x']:
        pos_direction['x_dir'] = 'left'
    else:
        pos_direction['x_dir'] = 'right'

    if cur_pos['y'] == closest_food['y']:
        pos_direction['y_dir'] = None
    elif cur_pos['y'] > closest_food['y']:
        pos_direction['y_dir'] = 'up'
    else:
        pos_direction['y_dir'] = 'down'
    
    return pos_direction
	
def cur_head(game):
    me = game['you']
    cur_head = me['body'][0]
    return cur_head	
	
def find_food(game):

    food_locations = game['board']['food']
    print(food_locations)
	
    return food_locations
	
def sort_food(game, food_locations):
    cur_head = game['you']['body'][0]
    for food in food_locations: 
        dist = abs(cur_head['x'] - food['x']) + abs(cur_head['y'] - food['y'])		
        food['dist'] = dist			
    print(food_locations)
    return food_locations

	

def is_move_safe(move, data):
    dead_end = is_dead_end(move, data, 10)
    if dead_end:
        return False
    return is_point_safe(convert_move_to_new_head(get_head(data["you"]), move), data)

def is_point_safe(point, data):
    board = data["board"]
    snakes = board["snakes"]

    if is_snake_space(point, board, snakes):
        # print("point ", point, " is a snake space")
        return False
    elif is_wall_space(point, board["width"], board["height"]):
        # print("point ", point, " is a wall space")
        return False
    else:
        return True

def get_adjacent_quadrant_densities(starting_point, data):
    board = data['board']
    # returns the adjacent quadrants
    # if a wall if in a quadrant, it is not returned as a viable quadrant
    quad_size = get_quadrant_size(board)
    # define a quadrant by it's top left and bottom right corners
    top_left_quad = { 
        'top_left': { 'x': starting_point['x'] - quad_size, 'y': starting_point['y'] - quad_size },
        'bottom_right': { 'x': starting_point['x'], 'y': starting_point['y'] }
    }
    top_right_quad = {
        'top_left': { 'x': starting_point['x'], 'y': starting_point['y'] - quad_size },
        'bottom_right': { 'x': starting_point['x'] + quad_size, 'y': starting_point['y'] }
    }
    bottom_left_quad = { 
        'top_left': { 'x': starting_point['x'] - quad_size, 'y': starting_point['y'] },
        'bottom_right': { 'x': starting_point['x'], 'y': starting_point['y'] + quad_size }
    }
    bottom_right_quad = { 
        'top_left': { 'x': starting_point['x'], 'y': starting_point['y'] },
        'bottom_right': { 'x': starting_point['x'] + quad_size, 'y': starting_point['y'] + quad_size}
    }

    quadrant_densities = [
        { "id": "top_left", "density": get_quadrant_density(top_left_quad, quad_size, data) },
        { "id": "top_right", "density": get_quadrant_density(top_right_quad, quad_size, data) },
        { "id": "bottom_left", "density": get_quadrant_density(bottom_left_quad, quad_size, data) },
        { "id": "bottom_right", "density": get_quadrant_density(bottom_right_quad, quad_size, data) }
    ]

    quadrant_densities.sort(key=lambda x: x['density'])

    return quadrant_densities

def get_quadrant_density(quadrant, quad_size, data):
    num_quad_squares = quad_size * quad_size
    full_squares = 0
    top_left = quadrant['top_left']
    bottom_right = quadrant['bottom_right']
    for x in range(top_left['x'], bottom_right['x']):
        for y in range(top_left['y'], bottom_right['y']):
            point = {'x': x,'y': y}
            if is_snake_space(point, data['board'], data['board']['snakes']) or is_wall_space(point, data['board']['width'], data['board']['height']):
                full_squares += 1
    return full_squares / num_quad_squares
                

def get_quadrant_moves(quadrant):
    if quadrant["id"] == "top_left":
        return ["left", "up"]
    elif quadrant["id"] == "top_right":
        return ["right", "up"]
    elif quadrant["id"] == "bottom_left":
        return ["down", "left"]
    else:
        return ["down", "right"]
    
   
def is_dead_end(move, data, epoch=1):
    directions = ['up', 'down', 'right', 'left']
    safe_directions = []

    # add move to body
    data_copy = copy.deepcopy(data)
    data_copy['you']['body'].insert(0, convert_move_to_new_head(data_copy['you']['body'][0], move))


    # find safe directions
    for d in directions:
        if not is_wall(d, data_copy) and not is_snake(d, data_copy):
            safe_directions.append(d)
    
    # end of recursion
    if epoch == 0 or len(safe_directions) == 0:
        return len(safe_directions) == 0
    else:
        dead_end = True
        for sd in safe_directions:
            dead_end = dead_end and is_dead_end(sd, data_copy, epoch-1)


        # check all safe directions to see if they are safe
        return dead_end
