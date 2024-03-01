import kontroller_input
import sys
import pygame
import math
from pygame.locals import *
#denne filen bør sorteres med delfiler snart.
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()

min_kontroller = kontroller_input.PygameKontroller()#må byttes ut med ekte kontroller etter hvert.

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))


# Function to read rhythm patterns from .pat files
def read_rhythm_pattern(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()
    
# Function to create falling blocks
def create_block(action):#Bokstaver reflekterer en direksjon på greia
    action = action.split(':')
    blocks.append(Block(action[1], action[0], 0))


def blitRotate(surf, image, pos, originPos, angle):#Credit to Rabbid76

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  
    # draw rectangle around the image
    pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

def AngleOfTwoVectors(point1,point2):#inputs arent techincally vectors but ok.
    vector1 = [point2[0] - point1[0], point2[1] - point1[1]]
    vector2 = [1, 0]  # Reference vector along x-axis

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Return 0 angle when one of the vectors is a zero vector
    
    signed_angle_radians = math.atan2(cross_product, dot_product)
    angle_degrees = math.degrees(signed_angle_radians)
    
    # Ensure the angle is positive
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees

class Player():
    def __init__(self,x ,y ) -> None:
        self.x, self.y = x, y
        self.tox, self.toy = x, y
        self.score = 100#perfect score at start, basically glorified HP

    def blitComponents(self):
        screen.blit(Wheel,(self.x-100,self.y-100))
        blitRotate(screen, shield_img, (self.x,self.y),(w_shield/2,h_shield/2),AngleOfTwoVectors([self.x,self.y],[self.x+self.tox,self.y+self.toy]))

    def Input(self, inx, iny):
        if abs(inx) > 0.1 or abs(iny) > 0.1:#no sufficient input = no change in direction
            self.tox, self.toy = inx, iny

class Block():
    def __init__(self, speed, angleOfAttack, attackWho):
      self.speed = speed
      self.dir = angleOfAttack
      self.target = attackWho
      print("New block:",speed,self.dir)

# Sample rhythm pattern files
rhythm_pattern_files = ["game files/patterns/beatmaster.pat"]
index = 0
tickdown = 0
players = [Player(200, 400), Player(800, 400)]
rhythm_pattern = read_rhythm_pattern(rhythm_pattern_files[index])
print(rhythm_pattern)

#midlertidig
Wheel = pygame.transform.scale(pygame.image.load("game files/assets/wheel.png"), (200,200))
shield_img = pygame.transform.scale(pygame.image.load("game files/assets/shield.png"), (200,200))
w_shield, h_shield = shield_img.get_size()
Shield = pygame.transform.scale(shield_img, (200,200))
# Game loop

#midlertidlig variabel
angle = 0
usex = 0
usey = 0
blocks = [] #no blocks yet
while True:
    #test-input
    keys = pygame.key.get_pressed() # Henter trykkede knapper
    x, y, knappJ, knappA, knappB = min_kontroller.hent(keys)
    mousex, mousey = pygame.mouse.get_pos()

    screen.fill((255, 255, 255))

    #mouse cursor
    screen.blit(Wheel,(mousex-100,mousey-100))
    
    for id, player in enumerate(players):#gjør det slik at hver player blir tildelt en kontroller de bruker i sin deklarasjon
        if id == 0:
            player.Input(mousex - player.x, mousey - player.y)
        elif id == 1:#midlertidig
            player.Input(x, y)
    
    for block in blocks:
        pass

        player.blitComponents()#draweverything
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            pass

    # Check if player input matches rhythm pattern

    #do action
    if tickdown <= 0:
      if index == len(rhythm_pattern):
        print("Last tick, song complete.")
        break
      print("new tick, index =",index,"; in:",rhythm_pattern[index])
      currentLine = rhythm_pattern[index].split('-')
      create_block(currentLine[0])
      index = index + 1
      tickdown = int(currentLine[1])

    tickdown = tickdown - 1#ticks for rythmpattern-reading, make it so it stays consistent with deltatime
    pygame.display.flip()
    fpsClock.tick(fps)