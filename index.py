import kontroller_input
import sys
import pygame
import math
from pygame.locals import *
#denne filen bør sorteres med delfiler snart.
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
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

def AngleOfTwoVectors(vector1,vector2):#gpt
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    cosine_angle = dot_product / (magnitude1 * magnitude2)
    cosine_angle = min(1, max(-1, cosine_angle))  # Ensure cosine value is within [-1, 1]
    angle_radians = math.acos(cosine_angle)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

# Sample rhythm pattern files
rhythm_pattern_files = ["patterns/beatmaster.pat"]
index = 0
tickdown = 0

rhythm_pattern = read_rhythm_pattern(rhythm_pattern_files[index])
print(rhythm_pattern)

#midlertidig
Wheel = pygame.transform.scale(pygame.image.load("assets/wheel.png"), (400,400))
shield_img = pygame.transform.scale(pygame.image.load("assets/shield.png"), (400,400))
w, h = shield_img.get_size()
Shield = pygame.transform.scale(shield_img, (400,400))
# Game loop

#midlertidlig variabel
angle = 0
while True:
    keys = pygame.key.get_pressed() # Henter trykkede knapper
    x, y, knappJ, knappA, knappB = min_kontroller.hent(keys)
    print(x,y,knappA,knappB)

    screen.fill((255, 255, 255))
    screen.blit(Wheel,(width/2-200,height/2-200))

    #Shield
    blitRotate(screen, shield_img, (width/2,height/2),(w/2,h/2),AngleOfTwoVectors([0,0],[x*10,y*10]))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            pass

    if keys[K_LEFT]:
        angle += 1
    if keys[K_RIGHT]:
        angle -= 1

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