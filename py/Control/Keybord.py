#control function
#可调用本地所有包, 仅被main.py调用
import pygame
def key_control(Item, event):
    if event.key == pygame.K_UP:
        Item.add_speed(addspeed = (0, -10)) 
    elif event.key == pygame.K_DOWN:
        Item.add_speed(addspeed = (0, 10)) 
    elif event.key == pygame.K_LEFT:
        Item.add_speed(addspeed = (-10, 0)) 
    elif event.key == pygame.K_RIGHT:
        Item.add_speed(addspeed = (10, 0)) 
    elif event.key == pygame.K_SPACE:
        Item.update_speed(speed = (0, 0)) 

def key_control_count(Item, event):
    if event.key == pygame.K_UP:
        Item.add_speed(addspeed = (0, 10)) 
    elif event.key == pygame.K_DOWN:
        Item.add_speed(addspeed = (0, -10)) 
    elif event.key == pygame.K_LEFT:
        Item.add_speed(addspeed = (10, 0)) 
    elif event.key == pygame.K_RIGHT:
        Item.add_speed(addspeed = (-10, 0)) 