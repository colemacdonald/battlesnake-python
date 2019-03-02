import bottle
import os
import random
import math
from queue import Queue
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
	game_id = data['game_id']
	board_width = data['width']
	board_height = data['height']
	
	#Create adjacency list
	adjList = createADJ(board_width, board_height)
	
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
	my_id = data['you']
	snakes = data['snakes']
	turn = data['turn']
	food = data['food']
	board_width = data['width']
	board_height = data['height']
	kill_flag = False
	
	#Get our snake
	for snake in snakes:
		if snake['id'] == my_id:
			my_snake = snake
			health = snake['health_points']
			
	#Head coordinates and coordinates of adjacent spaces
	my_head = my_snake['coords'][0]
	adjacent = getAdjacent(my_head)
	
	#Breadth first search on gameboard
	bfsINFO = doBFS(pointToVertex(my_head), adjList)
	
	#Determine which directions are clear to move
	viable_move = getViable(adjacent)

	if health < 0: #go get apple
		if len(food) > 0:
			distance = []
			target = []
		for i in range(len(food)):
			distance[i] = math.fabs(food[i][0] - my_head[0]) + math.fabs(food[i][1] - my_head[1])
			if i == 0:
				target = food[i]
			elif distance[i] < distance[i-1]:
				target = food[i]
		for dist in distance:
			if target > dist:
				target = dist
		if (my_head[0] > target[0]):    # If the food is to the left of the head
			if 'left' in viable_move:
				# Clear other viable moves
				viable_move = 'left' 
		elif (my_head[0] < target[0]):  # If the food is to the right of the head
			if 'right' in viable_move:
				# Clear other viable moves
				viable_move = 'right'
		elif (my_head[1] > target[1]):  # If the food is above the head
			if 'up' in viable_move:
				# Clear other viable moves
				viable_move = 'up'
		else:                           # If the food is below the head
			if 'down' in viable_move:
				# Clear other viable moves
				viable_move = 'down'

	else: #keep doing other stuff #TODO: Implement Snake behavioural AI

		for direction, coord in viable_move.items():
			if deadEnd(coord, my_head, count = 0):
				viable_move.pop(direction, None)
   

	
	#Pick Move
	if not viable_move.keys():
		move = 'UP'
	else:
		move = random.choice(viable_move.keys())
	
	#Response
	return {
		'move': move,
		'taunt': taunt
	}
#Convert cartesian coords to integer vertex reference
def pointToVertex(point):
	global board_width
	vertex = board_width * point[1] + point[0]
	return vertex
#Get 4 adjacent spaces to specified point
def getAdjacent(point):
	adjacent = {}
	adjacent['up'] = [point[0], point[1]-1]
	adjacent['down'] = [point[0], point[1]+1]
	adjacent['left'] = [point[0]-1, point[1]]
	adjacent['right'] = [point[0]+1, point[1]]
	return adjacent
#Return dict of viable moves given adjacent spaces. Avoids walls and snakes already in place
def getViable(adjacent):
	global snakes
	global board_width
	global board_height
	viable_move = {}
	for direction, coord in adjacent.items():
		viable_flag = True
		if coord[0] < 0 or coord[0] > (board_width - 1): #if X coord is a wall value don't include direction
			viable_flag = False
		elif coord[1] < 0 or coord[1] > (board_height - 1): #if Y coord is a wall value don't include direction
			viable_flag = False
		for snake in snakes:
			if viable_flag == False: #if coord == a point in previous snake then break
				break
			for point in snake['coords']: #compare coord to all body points of snake
				if point == coord: #if this point in snake == coord then don't include direction and break
					viable_flag = False
					break
		if viable_flag == True: #if viable flag is still true then add direction to possible moves	    	    	    	    	    	    
			viable_move[direction] = coord
	return viable_move
#calculates if alley is deadend or open ended
def deadEnd(currCoord, lastCoord, count):
	count+=1
	if count == 5: return False
	adjacent = getAdjacent(currCoord)
	viable = getViable(adjacent)
	for direction, coord in viable.items():
		if coord == lastCoord:
			viable.pop(direction, None)
	if not viable:
		return True
	else: 
		for direction, coord in viable.items():
			if not deadEnd(coord, currCoord, count):
				return False
		return True
#Returns adjacency list for specified board size.
def createADJ(width, height):
	adj = []
	for i in range(0, width*height):
		if i < width:
			if i % width == 0: adj.append([i+1, i+width])
			elif i % width == width - 1: adj.append([i-1, i+width])
			else: adj.append([i-1, i+1, i+width])
		elif i > ((width * height)- width - 1) and i < (width * height):
			if i % width == 0: adj.append([i-width, i+1])
			elif i % width == width - 1: adj.append([i-width, i-1])
			else: adj.append([i-width, i-1, i+1])
		else:
			if i % width == 0: adj.append([i-width, i+1, i+width])
			elif i % width == width - 1: adj.append([i-width,i-1, i+width])
			else: adj.append([i-width, i-1, i+1, i+width])
	return adj
#Returns bfsInfo on board given current head position. 
#bfsINFO = [(distance from source), (parent)]
def doBFS(source, adjList):
	queue = Queue()
	bfsINFO = [None for i in range(len(adjList))]
	bfsINFO[source] = [0, None]
	queue.put(source)
	while not queue.empty():
		parent = queue.get()
		for neighbour in adjList[parent]:
			if bfsINFO[neighbour] == None:
				queue.put(neighbour)
				bfsINFO[neighbour] = [bfsINFO[parent][0]+1,parent]
	return bfsINFO
	
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
