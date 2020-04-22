import pygame as pg
import os
import sys

pg.init()


# Game Screen Variables
WIDTH = 600
HEIGHT = 800
BOX_WIDTH = 196
BOX_HEIGHT = 196
TITLE = "TicTacToe - Brandyn Powell - Milestone Project 1"


# Color Values - RGB Tuple Format
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_GREEN = (0, 52, 0)
BUTTON_RED = (155, 0, 0)


# Setting some game variables
GAME_RECTS = 	{}

taken_spots = []


win_list = [[0, 3, 6], 
			[1, 4, 7], 
			[2, 5, 8], 
			[0, 1, 2], 
			[3, 4, 5], 
			[6, 7, 8], 
			[0, 4, 8],
			[2, 4, 6]]

GAME_LINES = {
	"Border 1"	:	[(0,200),(0,HEIGHT)],
	"Border 2"	:	[(598,200),(598,HEIGHT)],
	"Border 3"	:	[(0,798),(WIDTH,798)],
	"Line 1" 	: 	[(200,200),(200,HEIGHT)],
	"Line 2"	: 	[(400,200),(400,HEIGHT)],
	"Line 3"	:	[(0,200),(WIDTH, 200)],
	"Line 4"	:	[(0,400),(WIDTH, 400)],
	"Line 5" 	:	[(0,600),(WIDTH,600)]

	}



# Creating the display and a timer
game_screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


## Resets the two game variables that change throughout the game: The game_rects and the taken_spots
def reset_game():
	global taken_spots, GAME_RECTS
	taken_spots = ["", "", "", "", "", "", "", "", ""]

	GAME_RECTS = 	{
					"Top Left"		:		pg.Rect(2, 202, BOX_WIDTH, BOX_HEIGHT),
					"Top Center"	:		pg.Rect(202, 202, BOX_WIDTH, BOX_HEIGHT),
					"Top Right"		:		pg.Rect(402, 202, BOX_WIDTH, BOX_HEIGHT),
					"Mid Left"		:		pg.Rect(2, 402, BOX_WIDTH, BOX_HEIGHT),
					"Mid Center"	:		pg.Rect(202, 402, BOX_WIDTH, BOX_HEIGHT),
					"Mid Right"		:		pg.Rect(402, 402, BOX_WIDTH, BOX_HEIGHT),
					"Bottom Left"	:		pg.Rect(2, 602, BOX_WIDTH, BOX_HEIGHT),
					"Bottom Center"	:		pg.Rect(202, 602, BOX_WIDTH, BOX_HEIGHT),
					"Bottom Right"	:		pg.Rect(402, 602, BOX_WIDTH, BOX_HEIGHT)
					}

	return taken_spots, GAME_RECTS




## A function created to draw specific text with specified placement, font size, and color
def draw_text(font_size, text, antialias, color, center_position):
	new_font = pg.font.Font(None, font_size)
	new_text = new_font.render(text, antialias, color)
	new_text_rect = new_text.get_rect()
	new_text_rect.center = (int(center_position[0]), int(center_position[1]))
	game_screen.blit(new_text, new_text_rect)
	return new_text_rect




## A function to create pseudo buttons on the screen
def create_button(top_left_x, top_left_y, width, height, button_color, text_color, display_text, text_size):
	button = pg.Surface((width, height))
	button.fill(button_color)
	game_screen.blit(button, (int(top_left_x), int(top_left_y)))
	button_text = draw_text(text_size, display_text, True, text_color, ((top_left_x+int(width/2)), (top_left_y + int(height/2))))
	button_rect = button.get_rect()
	button_rect.center = (int(top_left_x+(width/2)), int(top_left_y + int(height/2)))
	return button_rect



## Displays the title bar above the game with the name and programmer
def display_title_bar():
	title_text_rect = draw_text(100, 'Tic Tac Toe', True, RED, (WIDTH//2, 50))
	subtitle_text_rect = draw_text(35, 'Code by Brandyn Powell', True, RED, (WIDTH//2, 90))
	pg.draw.line(game_screen, LINE_COLOR, (title_text_rect.left-10, subtitle_text_rect.bottom+5),(title_text_rect.right+10, subtitle_text_rect.bottom+5),2)




## Displays the player who's turn it currently is
def display_turn(player, symbol):
	pg.draw.rect(game_screen, BACKGROUND_COLOR, pg.Rect(2, 110, 600, 60))
	draw_text(24, f"{player}'s Turn! Player shape: {symbol}'s", True, LINE_COLOR, (WIDTH//2,120))




## Returns whether the specified player is either X's or O's
def get_player_shape(player):
	if player == "Player 1":
		return "X"
	else:
		return "O"




## Checks the taken spots against the win list to determine if someone has won
def check_for_winners():
	found_winner = False
	for win_way in win_list:
		if not found_winner:
			if taken_spots[win_way[0]] == taken_spots[win_way[1]] == taken_spots[win_way[2]] and taken_spots[win_way[0]] in ['X', 'O']:
				found_winner = True
				return True




## Receives the mouse click coords and determines the box the player clicked in and where
## to position his or her symbol.
def determine_image_location(mouse_x, mouse_y, rects, played_spots, player_symbol):
	for position, box in enumerate(rects.keys()):
		box_location = rects[box]
		if box_location not in ['X', 'O']:
			if mouse_x in range(box_location.x,box_location.x+box_location.width) and mouse_y in range(box_location.y, box_location.y+box_location.height):
				taken_spots[position] = player_symbol
				rects[box] = player_symbol
				return (box_location.centerx-int((box_location.width/2-10)), box_location.centery-int((box_location.height/2-10)))
	else:
		print("Invalid Placement. Try another location!")
		return None




## Drawing the lines on the screen. Borders and game lines are included.
def draw_lines():
	for line, position in GAME_LINES.items():
		pg.draw.line(game_screen, LINE_COLOR, position[0], position[1], 4)




## Displays a start screen to the user
def start_screen():
	game_screen.fill(BACKGROUND_COLOR)
	draw_text(120, "Tic Tac Toe", True, RED, (WIDTH/2, HEIGHT/2-250))
	pg.draw.line(game_screen, LINE_COLOR, (60, int(HEIGHT/2-215)), (WIDTH-60, int(HEIGHT/2-215)), 4)
	draw_text(50, "Udemy Section 7 Project", True, RED, (WIDTH/2, HEIGHT/2-190))
	pg.draw.line(game_screen, LINE_COLOR, (80, int(HEIGHT/2-170)), (WIDTH-80, int(HEIGHT/2-170)), 4)
	draw_text(35, "To play, click start!", True, LINE_COLOR, (WIDTH/2, HEIGHT/2-150))
	start_button = create_button(WIDTH/2-100, HEIGHT/2-110, 200, 60, BUTTON_GREEN, BACKGROUND_COLOR, "START!", 80)

	draw_text(35, "The rules are simple:", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+50))
	draw_text(35, "There are two players. Player 1", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+90))
	draw_text(35, "is the X and player 2 is the O.", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+130))
	draw_text(35, "Take turns on a 3x3 grid placing", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+170))
	draw_text(35, "your symbols. First person to 3", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+210))
	draw_text(35, "in a row vertically, horizontally,", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+250))
	draw_text(35, "or diagonally wins the game!", True, LINE_COLOR, (WIDTH/2, HEIGHT/2+290))

	start_game = False
	while not start_game:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			elif event.type == pg.MOUSEBUTTONDOWN and event.type != pg.QUIT:
				mouse_x, mouse_y = pg.mouse.get_pos()
				
				if mouse_x in range(start_button.x, start_button.x+start_button.width+1) and mouse_y in range(start_button.y, start_button.y+start_button.height):
					received_input = True
					game_loop()
				
			pg.display.update()



## Main game loop that brings together the above functions and lets the users play the game
def game_loop():
	taken_spots, GAME_RECTS = reset_game()
	game_over = False
	game_screen.fill(BACKGROUND_COLOR)
	draw_lines()
	display_title_bar()

	while not game_over:
		pg.display.update()
		clock.tick(60)
		
				

		for player in ["Player 1", "Player 2"]:
			symbol = get_player_shape(player)
			display_turn(player, symbol)
			turn_over = False
			pg.display.flip()

			while not turn_over:

				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
						sys.exit()
						game_over = True

					elif event.type == pg.MOUSEBUTTONDOWN and event.type != pg.QUIT:
						mouse_x, mouse_y = pg.mouse.get_pos()
						loaded_image = pg.image.load(os.path.relpath(f"{symbol}"+".png", start=os.curdir))
						image_location = determine_image_location(mouse_x, mouse_y, GAME_RECTS, taken_spots, symbol)
						if image_location == None:
							break
						else:
							game_screen.blit(loaded_image, image_location)
							pg.display.update()
							winning_player = player
							turn_over = True

			if check_for_winners():
				winner = f"{symbol}'s win!"
				game_over = True
				break
			elif "" not in taken_spots:
				winner = "It's a tie!"
				game_over = True
				break


	play_again_screen(winner)




## Shows a game over screen and gets input on whether the user would like to play again
def play_again_screen(winner):
	game_screen.fill(BACKGROUND_COLOR)
	draw_text(120, "GAME OVER!", True, LINE_COLOR, (WIDTH/2, HEIGHT/2-200))
	draw_text(50, winner, True, LINE_COLOR, (WIDTH/2, HEIGHT/2-100))
	draw_text(35, f"Play Again?", True, LINE_COLOR, (WIDTH/2, HEIGHT/2))
	rematch_button = create_button(100, HEIGHT/2+50, 80, 30, BUTTON_GREEN, BACKGROUND_COLOR, "Rematch!", 20)
	not_now_button = create_button(400, HEIGHT/2+50, 80, 30, BUTTON_RED, BACKGROUND_COLOR, "Not now :(", 20)


	received_input = False
	while not received_input:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			elif event.type == pg.MOUSEBUTTONDOWN and event.type != pg.QUIT:
				mouse_x, mouse_y = pg.mouse.get_pos()

				if mouse_x in range(rematch_button.x, rematch_button.x+rematch_button.width+1) and mouse_y in range(rematch_button.y, rematch_button.y+rematch_button.height):
					received_input = True
					game_loop()

				elif mouse_x in range(not_now_button.x, not_now_button.x+not_now_button.width+1) and mouse_y in range(not_now_button.y, not_now_button.y+not_now_button.height):
					pg.quit()
					sys.exit()
				
			pg.display.update()
						



if __name__ == "__main__":
	start_screen()
	game_loop()
	play_again()
