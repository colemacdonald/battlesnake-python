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


def is_snake(move, game):
    # board data
    width = game['board']['width']
    height = game['board']['height']

    # snakes
    snakes = game['snakes']
    me = game['you']

    cur_head = me['body'][0]
    new_head = convert_move_to_new_head(cur_head, move)

    for snake in snakes:
        for square in snake['body']:
            if is_same_space(new_head):
                return True

    return False
    