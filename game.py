### **Функционал**

# - Реализовать возможность рисовать мышкой ok
# - Высвечивать ошибку, если игрок рисует слишком близко к точке ok
# - Высвечивать ошибку, если игрок рисует слишком медленно ok
# - Демонстрировать в процентах насколько круг идеален ok 
# - По мере ухудшения качества круга изменять цвет в более красный ok

import pygame
import math
import numpy as np


clock = pygame.time.Clock()
# Makings screen
screen = pygame.display.set_mode((900, 700))
 
# Setting Title
pygame.display.set_caption('Draw perfect circle')
 
# put dot in the middle of canvas
circle_color = (255,255,0)
ycircle = 350
xcircle = 450
draw_on = False
last_pos = (0, 0) 
ideal_radius=0

# Radius of the Brush
radius = 3
 
# score
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

# time
clock = pygame.time.Clock()


# function to drow smooth line (function taken from https://www.geeksforgeeks.org/how-to-create-ms-paint-clone-with-python-and-pygame/ )
def roundline(canvas, color, start, end, radius=1):
    Xaxis = end[0]-start[0]
    Yaxis = end[1]-start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0]+float(i)/dist*Xaxis)
        y = int(start[1]+float(i)/dist*Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)
 

# x coord of the motion and y coord of motion
x_coord = []
y_coord = [] 

x_r2_list = []
y_r2_list = []

try:
    while True:
        pygame.draw.circle(screen, circle_color, (xcircle, ycircle), 10)
        pygame.display.update()
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        # movement of mouse 
        mouse_pos = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEBUTTONDOWN:         
            # Selecting Color Code
            color = (0,250,0)
            # Draw a single circle wheneven mouse is clicked down.
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
            start_time = pygame.time.get_ticks()
        # When mouse button released it will stop drawing   
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 900, 700))
            pygame.display.update()
        if pygame.mouse.get_pressed()[0]:   
            # окрашивание цвета при близком расстоянии
            if math.sqrt((mouse_pos[0]-xcircle)**2+(mouse_pos[1]-ycircle)**2)<50:
                color = (255,0,0)
            else: 
                color = (0,255,0)   
            if abs(math.sqrt((mouse_pos[0]-xcircle)**2+(mouse_pos[1]-ycircle)**2)-ideal_radius)>60:
                color = (255,0,0)
            else: 
                color = (0,255,0)   
            # время нажатия t>7s ошибка
            time_since_enter = pygame.time.get_ticks() - start_time
            if time_since_enter>7000:
                screen.blit(font.render('Too slow', True, (0,255,0)), (100, 100))
                pygame.display.update()
                pygame.time.wait(3000)
            # calculating ideal radius
            x_coord.append(mouse_pos[0])
            y_coord.append(mouse_pos[1])
            ideal_radius = math.sqrt((x_coord[0]-xcircle)**2+(y_coord[0]-ycircle)**2)
            x_coord_rel = [(x-xcircle)**2 for x in x_coord]
            y_coord_rel = [(y-ycircle)**2 for y in y_coord]
            real_rad_sqrt = np.add(np.array(x_coord_rel), np.array(y_coord_rel))
            real_radius_array = np.sqrt(real_rad_sqrt)
            real_radius = np.average(real_radius_array)
            # percent of how good circle is: error = (experimental-actual)/actual
            perc_result = 100-abs((ideal_radius - real_radius)/real_radius*100)
            print(perc_result)
            # Draw the score to the screen
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 170, 60))
            score_text = font.render(f'Score: {int(perc_result)}%', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            pygame.display.update()
        # It will draw a continuous circle with the help of roundline function.   
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos,  radius)
        # collecting position of mouse when its pressed
            last_pos = e.pos
        # Limit the frame rate
        clock.tick(100)

except StopIteration:
    pass
   

# Quit
pygame.quit()
