import bottle
import os
import random
import math
from queue import Queue
import pdb
my_name = "elttab ekans"
color = "#234864"
taunt = "Get some!"
ajdList = []


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
	#Globals
	global board_width
	global board_height
	global adjList
	
	#Post Data
	data = bottle.request.json
	game_id = data['game']['id']
	board = data['board']
	board_width = board['width']
	board_height = board['height']
		
	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
		)

	
	#Response
	return {
		'color': color,
		'taunt': taunt,
		'head_url': head_url,
		'name': my_name
	}


@bottle.post('/move')
def move():
	#Globals
	global board_width
	global board_height
	global snakes
	global adjList
	
	#Get request data
	data = bottle.request.json
	my_id = data['you']['id']
	board = data['board']
	snakes = board['snakes']
	turn = data['turn']
	food = board['food']
	board_width = board['width']
	board_height = board['height']
	kill_flag = False
	
	#Get our snake
	for snake in snakes:
		if snake['id'] == my_id:
			my_snake = snake
			health = snake['health']
			
	#Head coordinates and coordinates of adjacent spaces
	my_head = my_snake['body'][0]

	#Response
	return {
		'move': 'right',
		'taunt': taunt
	}

	
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
