import random
import math

# contains some utility functions for getting information about the board / potential moves

from operator import itemgetter, attrgetter, methodcaller 


def is_same_space(space1, space2):
    return (space1['x'] == space2['x'] and space1['y'] == space2['y'])


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

def need_food(data):
    me = data['you']
    health = me['health']
    #closest_food = find_food()
    closest_food = { 
        'x':1, 
        'y':1
    }
    distance_to_food = closest_food['x'] + closest_food['y']
    print("***************")
    print(distance_to_food)
    print(health)
    if health < distance_to_food:
        return True
    else:
         return False

def get_food(data, direction):
    #direction = find_safe_move(data)
    closest_food = {
        'x': 1, 
        'y': 1
    }
    me = data['you']

    head = me['body'][0]
    new_head = convert_move_to_new_head(head, direction)

    head_to_food = head - closest_food
    move_to_food = new_head - closest_food
    if (move_to_food <= head_to_food):
        return direction
    else: 
        get_food(data, find_safe_move(data))

	
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
	
	
