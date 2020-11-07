#!/usr/bin/env python

import pygame, sys
from pygame.locals import *
from random import randrange
import time
from typing import *


# blue represents player 1, and red prepresents player 2
# dot positions are represented in such a way that dots will travel on the upper right corner of each square
class Game:
    def __init__(self, int_player1_position, int_player2_position, ladders_dict, snakes_dict, DISPLAY):
        self.int_player1_position = int_player1_position # set to 0 when initiate
        self.int_player2_position = int_player2_position # set to 0 when initiate
        self.ladders_dict = ladders_dict
        self.snakes_dict = snakes_dict
        self.DISPLAY = DISPLAY

    def throw_dice(self) -> int:
        """simulate die throwing."""
        return randrange(1, 6)


    def current_status(self, int_player1_position:int, int_player2_position:int) -> (int, int):
        """function takes in positions of both players and returns the next
        position of players as the game progresses. If the player enters a square
        that's in the snakes and ladders region, it will be directed to the appropriate
        places."""

        self.int_player1_position = self.int_player1_position + self.throw_dice()
        self.int_player2_position = self.int_player2_position + self.throw_dice()

        # check if the player is encountering ladders
        if self.int_player1_position in self.ladders_dict:
            self.int_player1_position = self.ladders_dict[self.int_player1_position]
        if self.int_player1_position in self.snakes_dict:
            self.int_player1_position = self.snakes_dict[self.int_player1_position]
        
        # check if the player is encountering snakes
        if self.int_player2_position in self.ladders_dict:
            self.int_player2_position = self.ladders_dict[self.int_player2_position]
        if self.int_player2_position in self.snakes_dict:
            self.int_player2_position = self.snakes_dict[self.int_player2_position]

        return self.int_player1_position, self.int_player2_position


    def play_game(self) -> None:
        """function initializes the game and plays one step of the game
        per frame."""

        BLACK = (0,0,0)
        time.sleep(2)

        # if no one has won the game, then continue to the next step
        if self.int_player1_position < 100 and self.int_player2_position < 100:
            self.int_player1_position, self.int_player2_position = self.current_status(self.int_player1_position, self.int_player2_position)


    def draw_game(self) -> None:
        """Main function that calls all functions."""
        WHITE=(255,255,255)
        BLUE=(0,0,255)

        self.DISPLAY.fill(WHITE)

        self.play_game()
        self.draw_board(0, 0)
        self.draw_circle()
        self.draw_text(900, 0)
        self.draw_lines()
        self.draw_winner()


    def draw_board(self, x:int, y:int) -> None:
        """draws and renders a 1000 by 1000 board."""
        BLACK=(0,0,0)
        width = 100
        length = 100
        while y <= 1000:
            while x <= 1000:
                pygame.draw.rect(self.DISPLAY,BLACK,(x,y,100,100), 5)
                x = x + width
            y = y + length
            x = 0


    def draw_circle(self) -> None:
        """draws the circle based on player 1 and player 2's positions.
        Player 1 is blue and player 2 is red."""
        BLUE=(0,0,255)
        RED = (225,0,0)

        final_x_1 = self.int_player1_position % 10 * 100
        final_y_1 = (9 - self.int_player1_position // 10) * 100
        pygame.draw.circle(self.DISPLAY, BLUE, (final_x_1, final_y_1), 20)

        final_x_2 = self.int_player2_position % 10 * 100
        final_y_2 = (9 - self.int_player2_position // 10) * 100
        pygame.draw.circle(self.DISPLAY, RED, (final_x_2, final_y_2), 20)


    def draw_text(self, x:int, y:int) -> None:
        """draws numers that fill the board. Numbers range from 1 to 100"""
        BLACK=(0,0,0)
        width = 100
        length = 100
        current_number = 100
        while y <= 1000:
            while x >= 0:
                font = pygame.font.SysFont(str(current_number), 40)
                img = font.render(str(current_number), True, BLACK)
                self.DISPLAY.blit(img, (x, y))
                current_number = current_number - 1
                x = x - width
            y = y + length
            x = 900


    def draw_lines(self) -> None:
        """draws snakes and ladders on the board. Green lines represent ladders
        and purple lines represent snakes."""
        GREEN = (0,200,0)
        PURPLE = (102,0,102)

        for idx, num in self.ladders_dict.items():
            x_coord_start = idx % 10 * 100
            y_coord_start = (9 - idx // 10) * 100
            if num != 100: # makes an exception for 100 as modulus and long division don't behave correctly according to the game
                x_coord_end = num % 10 * 100
                y_coord_end = (9 - num // 10) * 100
            if num == 100:
                x_coord_end = 1000
                y_coord_end = 0
            pygame.draw.line(self.DISPLAY, GREEN, (x_coord_start, y_coord_start), (x_coord_end, y_coord_end), 10)

        for idx, num in self.snakes_dict.items():
            x_coord_start = idx % 10 * 100
            y_coord_start = (9 - idx // 10) * 100
            x_coord_end = num % 10 * 100
            y_coord_end = (9 - num // 10) * 100
            pygame.draw.line(self.DISPLAY, PURPLE, (x_coord_start, y_coord_start), (x_coord_end, y_coord_end), 10)

        
    def draw_winner(self):
        """Displays text that announces the winner of the game"""
        BLACK = (0,0,0)
        if self.int_player1_position >= 100:
            font1 = pygame.font.SysFont('winner is player 1', 150)
            img1 = font1.render('winner is player 1', True, BLACK)
            self.DISPLAY.blit(img1, (50, 400))

        if self.int_player2_position >= 100:
            font1 = pygame.font.SysFont('winner is player 2', 150)
            img1 = font1.render('winner is player 2', True, BLACK)
            self.DISPLAY.blit(img1, (50, 400))


    def main(self) -> None:
        """Main function that provides background for drawing and renders draw_game(),
        which in turn plays the game and shows the simulation of the game on a board
        in pygame"""
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_game()

            pygame.display.update()

# setting up variables to feed into instance variables
ladders = {1:38, 4:14, 9:31, 28:84, 36:47, 21:42, 51:67, 71:91, 80:100}
snakes = {16:6, 49:11, 47:26, 56:53, 62:19, 64:60, 87:24, 93:73, 95:75, 98:78}
display = pygame.display.set_mode((1000,1000), 0, 32)

# calling main() function to start the whole program
game = Game(0, 0, ladders, snakes, display)
game.main()