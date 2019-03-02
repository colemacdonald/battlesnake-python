# contains some utility functions for getting information about the board / potential moves


def convert_move_to_new_head(cur_head, move):
    if move == 'up':
        return {'x': cur_head['x'], 'y': cur_head['y'] - 1}
    elif move == 'down':
        return {'x': cur_head['x'], 'y': cur_head['y'] + 1}
    elif move == 'right':
        return {'x': cur_head['x'] + 1, 'y': cur_head['y']}
    elif move == 'left':
        return {'x': cur_head['x'] - 1, 'y': cur_head['y']}


def is_enemy(move, game):
    # board data
    width = game['board']['width']
    height = game['board']['height']

    # snakes
    snakes = game['snakes']
    me = game['you']


    