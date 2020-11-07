#!/usr/bin/env python

import pygame, sys
from pygame.locals import *
from random import randrange
import time
from typing import *


# blue represents player 1, and red prepresents player 2
# dot positions are represented in such a way that dots will travel on the upper right corner of each square

# using dictionaries to represent snakes and ladders used in game
ladders_dict = {1:38, 4:14, 9:31, 28:84, 36:47, 21:42, 51:67, 71:91, 80:100}
snakes_dict = {16:6, 49:11, 47:26, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 98:78}

def throw_dice() -> int:
    """simulate die throwing."""
    return randrange(1, 6)

# setting up global variables for the position of players
int_player1_position = 0
int_player2_position = 0


def current_status(player1_position:int, player2_position:int) -> (int, int): # not sure about the typing for this one...
    """function takes in positions of both players and returns the next
    position of players as the game progresses. If the player enters a square
    that's in the snakes and ladders region, it will be directed to the appropriate
    places."""
    global int_player1_position
    global int_player2_position

    int_player1_position = player1_position + throw_dice()
    int_player2_position = player2_position + throw_dice()

    # check if the player is encountering ladders
    if int_player1_position in ladders_dict:
        int_player1_position = ladders_dict[int_player1_position]
    if int_player1_position in snakes_dict:
        int_player1_position = snakes_dict[int_player1_position]
    
    # check if the player is encountering snakes
    if int_player2_position in ladders_dict:
        int_player2_position = ladders_dict[int_player2_position]
    if int_player2_position in snakes_dict:
        int_player2_position = snakes_dict[int_player2_position]

    return int_player1_position, int_player2_position


def play_game() -> None:
    """function initializes the game and plays one step of the game
    per frame."""
    global int_player1_position
    global int_player2_position

    BLACK = (0,0,0)
    time.sleep(2)

    # if no one has won the game, then continue to the next step
    if int_player1_position < 100 and int_player2_position < 100:
        int_player1_position, int_player2_position = current_status(int_player1_position, int_player2_position)


DISPLAY = pygame.display.set_mode((1000,1000), 0, 32)


def draw_game() -> None:
    """Main function that calls all functions."""
    WHITE=(255,255,255)
    BLUE=(0,0,255)

    DISPLAY.fill(WHITE)

    play_game()
    draw_board(0, 0)
    draw_circle()
    draw_text(900, 0)
    draw_lines()
    draw_winner()


def draw_board(x:int, y:int) -> None:
    """draws and renders a 1000 by 1000 board."""
    BLACK=(0,0,0)
    width = 100
    length = 100
    while y <= 1000:
        while x <= 1000:
            pygame.draw.rect(DISPLAY,BLACK,(x,y,100,100), 5)
            x = x + width
        y = y + length
        x = 0


def draw_circle() -> None:
    """draws the circle based on player 1 and player 2's positions.
    Player 1 is blue and player 2 is red."""
    BLUE=(0,0,255)
    RED = (225,0,0)

    final_x_1 = int_player1_position % 10 * 100
    final_y_1 = (9 - int_player1_position // 10) * 100
    pygame.draw.circle(DISPLAY, BLUE, (final_x_1, final_y_1), 20)

    final_x_2 = int_player2_position % 10 * 100
    final_y_2 = (9 - int_player2_position // 10) * 100
    pygame.draw.circle(DISPLAY, RED, (final_x_2, final_y_2), 20)


def draw_text(x:int, y:int) -> None:
    """draws numers that fill the board. Numbers range from 1 to 100"""
    BLACK=(0,0,0)
    width = 100
    length = 100
    current_number = 100
    while y <= 1000:
        while x >= 0:
            font = pygame.font.SysFont(str(current_number), 40)
            img = font.render(str(current_number), True, BLACK)
            DISPLAY.blit(img, (x, y))
            current_number = current_number - 1
            x = x - width
        y = y + length
        x = 900


def draw_lines() -> None:
    """draws snakes and ladders on the board. Green lines represent ladders
    and purple lines represent snakes."""
    GREEN = (0,200,0)
    PURPLE = (102,0,102)

    for idx, num in ladders_dict.items():
        x_coord_start = idx % 10 * 100
        y_coord_start = (9 - idx // 10) * 100
        if num != 100: # makes an exception for 100 as modulus and long division don't behave correctly according to the game
            x_coord_end = num % 10 * 100
            y_coord_end = (9 - num // 10) * 100
        if num == 100:
            x_coord_end = 1000
            y_coord_end = 0
        pygame.draw.line(DISPLAY, GREEN, (x_coord_start, y_coord_start), (x_coord_end, y_coord_end), 10)

    for idx, num in snakes_dict.items():
        x_coord_start = idx % 10 * 100
        y_coord_start = (9 - idx // 10) * 100
        x_coord_end = num % 10 * 100
        y_coord_end = (9 - num // 10) * 100
        pygame.draw.line(DISPLAY, PURPLE, (x_coord_start, y_coord_start), (x_coord_end, y_coord_end), 10)

    
def draw_winner():
    """Displays text that announces the winner of the game"""
    BLACK = (0,0,0)
    if int_player1_position >= 100:
        font1 = pygame.font.SysFont('winner is player 1', 150)
        img1 = font1.render('winner is player 1', True, BLACK)
        DISPLAY.blit(img1, (50, 400))

    if int_player2_position >= 100:
        font1 = pygame.font.SysFont('winner is player 2', 150)
        img1 = font1.render('winner is player 2', True, BLACK)
        DISPLAY.blit(img1, (50, 400))


def main() -> None:
    """Main function that provides background for drawing and renders draw_game(),
    which in turn plays the game and shows the simulation of the game on a board
    in pygame"""
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_game()

        pygame.display.update()

# calling main() function to start the whole program.
main()