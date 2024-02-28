import kontroller_input
import sys
import pygame
import math
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()


min_kontroller = kontroller_input.TestKontroller()#må byttes ut med ekte kontroller etter hvert.


width, height = 1024, 768
screen = pygame.display.set_mode((width, height))


# Function to read rhythm patterns from .pat files
def read_rhythm_pattern(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()
class Block():
    def __init__(self, speed, dir):
      self.speed = speed
      self.dir = dir
      print("New block",speed,dir)

def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect
# Function to create falling blocks
def create_block(action):#Bokstaver reflekterer en direksjon på greia
    action = action.split(':')
    Block(action[1], action[0])

    

# Function to handle button presses
def handle_button_press():
    # Placeholder for now, you would implement this
    pass

# Function to check if player input matches rhythm pattern
def check_input(rhythm_pattern):
    # Placeholder for now, you would implement this
    pass

# Sample rhythm pattern files
rhythm_pattern_files = ["patterns/beatmaster.pat"]
index = 0
tickdown = 0

rhythm_pattern = read_rhythm_pattern(rhythm_pattern_files[index])
print(rhythm_pattern)

#midlertidig
Wheel = pygame.transform.scale(pygame.image.load("assets/wheel.png"), (400,400))
Shield = pygame.transform.scale(pygame.image.load("assets/shield.png"), (400,400))
# Game loop
while True:
    keys = pygame.key.get_pressed() # Henter trykkede knapper
    x, y, knappJ, knappA, knappB = min_kontroller.hent(keys)
    print(x,y,knappA,knappB)

    screen.fill((255, 255, 255))
    screen.blit(Wheel,(width/2-200,height/2-200))
    #Rect
    screen.blit(Shield,(0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            handle_button_press()

    # Check if player input matches rhythm pattern

    #do action
    '''if tickdown <= 0:
      if index == len(rhythm_pattern):
        print("Last tick, song complete.")
        break
      print("new tick, index =",index,"; in:",rhythm_pattern[index])
      currentLine = rhythm_pattern[index].split('-')
      create_block(currentLine[0])
      index = index + 1
      tickdown = int(currentLine[1])'''

    tickdown = tickdown - 1
    # Update screen
    pygame.display.flip()
    fpsClock.tick(fps)