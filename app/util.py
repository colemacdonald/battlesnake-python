import random
import copy

# contains some utility functions for getting information about the board / potential moves

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
    new_head = convert_move_to_new_head(cur_head, move)

    for snake in snakes:
        for square in snake['body']:
            if is_same_space(new_head, square):
                return True

    return False


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
        dead_end = is_dead_end(d, data, 5)
        print('Turn %d, move: %s. Is dead end? %s' % (data['turn'], d, dead_end))
        if not is_wall(d, data) and not is_snake(d, data) and not dead_end:
            return d

        safe_directions.remove(d)
    
    return 'up'
    
   
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
        print("Epoch: %d" % epoch)
        print(safe_directions)
        print(data_copy['you']['body'])
        for sd in safe_directions:
            dead_end = dead_end and is_dead_end(sd, data_copy, epoch-1)


        # check all safe directions to see if they are safe
        return dead_end