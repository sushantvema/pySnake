import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os

""" Welcome to the game code for 'pySnake'. The user_input function below takes in an integer the user inputs at the start of the game
and uses it later to get the number of rows depending on the difficulty"""
def user_input():
	root = tk.Tk()
	root.withdraw()
	difficulty_string = simpledialog.askinteger("Welcome to pySnake! by Sushant Vema '24 and Saikrishna Achalla '24", "What is your preferred difficulty? \n" + "Please select a number between 0 and 10 where 0 is easy and 10 is hard.", parent=root, minvalue=0, maxvalue=10)
	return 20 - difficulty_string

var_rows = user_input()

class cube(object):
	rows = var_rows
	w = 35 * rows
	"""Below are random numbers to determine the color of the snake. We intentionally restricted the range of values for the green color
	because the snack that is placed at random positions is also green and so we did not want any confusion"""
	rand_red = random.randrange(5, 255)
	rand_green = random.randrange(5, 150)
	rand_blue = random.randrange(5, 255)

	def __init__(self,start,dir_x=1,dir_y=0,color=(rand_red, rand_green, rand_blue)):
		self.pos = start
		self.dir_x = 1
		self.dir_y = 0
		self.color = color
	""" dir_x and dir_y are the (x,y) directions in which the snake moves respectively. +1 in x direction means it's moving to the right.
	+1 in the y direction means it's moving to upwards."""
	def move(self, dir_x, dir_y):
		self.dir_x = dir_x
		self.dir_y = dir_y
		""" The code below returns the new position for the snake after a certain direction arrow is pressed. It basically adds the
		existing (x,y) position of the snake to the dir_x and dir_y respectively."""
		self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

	def draw(self, surface):
		""" dist_bw_box is the number of cubes that are in the row/column since the game board is a square. I use floor division to avoid
		non-whole numbers because that would cause the grid not to have a whole number of cubes."""
		dist_bw_box = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
		""" This line draws the cube which is the body of the snake as well as the randomly placed snack. The third argument in the
		rect function is the (x,y) coordinates of the top left of the rectangle and the height and width of the rectangle. In this case,
		I have the top left corner at (1,1) respective to the block being drawn in. This is so that the color fill does not cover the
		grid lines """
		pygame.draw.rect(surface, self.color, (i*dist_bw_box+1,j*dist_bw_box+1, dist_bw_box-2, dist_bw_box-2))

class snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dir_x = 0
		self.dir_y = 1

	def move(self):

		for event in pygame.event.get():
			""" If the player clicks on the exit button in the top right corner of the game, the game closes"""
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			keys = pygame.key.get_pressed()

			for key in keys:
				""" In each of the instances below, We are changing the direction in which the head, which is the first block in the
				direction of motion of the snake, moves."""
				if keys[pygame.K_LEFT]:
					self.dir_x = -1
					self.dir_y = 0
					self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

				elif keys[pygame.K_RIGHT]:
					self.dir_x = 1
					self.dir_y = 0
					self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

				elif keys[pygame.K_UP]:
					self.dir_x = 0
					self.dir_y = -1
					self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

				elif keys[pygame.K_DOWN]:
					self.dir_x = 0
					self.dir_y = 1
					self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
					""" This code allows for wrapping of the snake around the board """
			else:
				if c.dir_x == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
				elif c.dir_x == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
				elif c.dir_y == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
				elif c.dir_y == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
				else: c.move(c.dir_x,c.dir_y)

	"""This function re-initializes the Snake upon a game restart."""
	def reset(self, pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dir_x = 0
		self.dir_y = 1

	"""This function and the conditions below are to add a cube to the end of the snake when necessary, depending on the direction in which the snake is moving."""
	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dir_x, tail.dir_y
		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

		self.body[-1].dir_x = dx
		self.body[-1].dir_y = dy


	def draw(self, surface):
		for i, c in enumerate(self.body):
			c.draw(surface)

"""This function is our algorithm for drawing a perfectly proportional grid based solely on a pixel measurement of width,
and number of desired rows (based on difficulty)."""
def drawGrid(w, rows, surface):
	sizeBtwn = w // rows

	x = 0
	y = 0
	for l in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn

		pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
		pygame.draw.line(surface, (255,255,255), (0,y),(w,y))


"""This function re-initializes the board upon a game restart."""
def redrawWindow(surface):
	global rows, width, s, snack
	surface.fill((0,0,0))
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width,var_rows, surface)
	pygame.display.update()

"""This function randomly outputs a coordinate value in which to spawn a snack, while making sure that the snack will not
ever overlap with the body of the snake."""
def randomSnack(rows, item):

	positions = item.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break

	return (x,y)

"""This function implements functionality from a Python package called tkinter, allowing us to produe robust graphical message popups when need-be."""
def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass

"""The following is our main() code, which effectively controls the logic of the game progression."""
def main():

	global width, rows, s, snack

	"""This block of code initializes various values and objects and sets the game in motion."""
	random_start = random.randrange(var_rows)
	rows = var_rows
	width = 35 * var_rows
	win = pygame.display.set_mode((width, width))
	s = snake((255,0,0), (random_start, random_start))
	snack = cube(randomSnack(rows, s), color=(0,255,0))
	flag = True

	"""The following code is our implementation of 'difficulty gradients' in speed. As the snake's length passes certain
	thresholds, the game speed will be increased."""
	clock = pygame.time.Clock()
	while flag:
		if var_rows >= 15:
			if len(s.body) <= 10:
				pygame.time.delay(25)
				clock.tick(10)
			elif len(s.body) <= 20:
				pygame.time.delay(25)
				clock.tick(14)
			elif len(s.body) <= 30:
				pygame.time.delay(25)
				clock.tick(18)
		if var_rows >= 10:
			if len(s.body) <= 10:
				pygame.time.delay(50)
				clock.tick(8)
			elif len(s.body) <= 15:
				pygame.time.delay(50)
				clock.tick(10)
			elif len(s.body) <= 20:
				pygame.time.delay(50)
				clock.tick(12)

		s.move()

		"""This conditional checks if the snake is about the consume a snack, and if so, proceeds to create a new snack to replace the old one
		so one snack will always be available at any time."""
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows, s), color=(0,255,0))

		"""The following for loop checks to see if the snake has hit itself. If it has, it will set in motion end-of-game processes and will
		ask user if they want to restart the game."""
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):

				message_box("SCORE:", "Your final score is " + str(len(s.body)) + ".")

				yes_or_no = messagebox.askyesno("GAME OVER","Would you like to play again?\nExit and restart the game if you'd like to change the difficulty.")

				if yes_or_no == True:
					message_box("Welcome Back to pySnake!", "Click the window to resume playing the game.")
					new_random_start = random.randrange(var_rows)
					s.reset((new_random_start, new_random_start))
					break
				else:
					pygame.quit()
					exit()

		redrawWindow(win)
	pass



main()
