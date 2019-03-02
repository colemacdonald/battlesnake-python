# contains some utility functions for getting information about the board / potential moves

def is_same_space(space1, space2):
    return space1['x'] == space2['x'] and space1['y'] == space2['y']


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
