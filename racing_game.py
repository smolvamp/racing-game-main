
import pygame as k
import time
#initating pygame
k.init()

#making window:
screen=k.display.set_mode((1000,400))
icon= k.image.load('icon.jpg')
k.display.set_icon(icon)
k.display.set_caption('Forza Horizon VI')

#car:
car = k.image.load('car.png')
carx= 72
cary= 128
carx_change= 0
cary_change= 0

#defining this shit to appear on screen on given coordinates:
def carimg(x,y):
    screen.blit(car, (x,y))

# Enemy cars
obs = k.image.load('obstacle.png')
obs2= k.image.load('jeep.png')
obsx = 1050
obsy = 50
obsx_change = -0.8
obsy_change = 0
obsx2 = 1350
obsy2= 250
obsx2_change = -0.8
obsy2_change = 0

# this function will make obstacle car appear on screen.
def obsimg(x, y):
    screen.blit(obs, (x, y))

def obs2img(x,y):
    screen.blit(obs2, (x, y))

#font:
font = k.font.Font(None, 36)
font2 = k.font.Font(None, 40)
font3 = k.font.Font(None, 100)

#collision:
def check_collision(x1, y1, x2, y2):
    if x2 == obsx:
        return (x1+128 < x2 + 64 and x1+128  > x2  and
                y1< y2+64  and y1 > y2-128)
    elif x2 == obsx2:
        return (x1+128 < x2 + 64 and x1+128  > x2  and
                y1 < y2 +64 and y1 > y2-64)
    else:
        return False

score= 0
obs_speed = 1
speed_increment = 0.08
running_game= False
controls= False

#intro function:
def intro_screen():
    #making buttons, and marking selected button.
    k.display.set_caption('Forza Horizon VI')
    selected_button = 'start' 
    start = font2.render("START", True, (0, 0, 0))
    quit_button = font2.render("QUIT", True, (0, 0, 0))
    controls = font2.render("CONTROLS", True, (0, 0, 0))
    selected_color = (255, 0, 0)
    button_color = (0, 0, 0)
    intro= True
    while intro:
        #intro add krte hue hum hehe hehe heh:
        ibg = k.image.load("ibg.jpg")
        screen.blit(ibg, (0, 0))

        for event in k.event.get():
            if event.type== k.QUIT:
                intro= False
                quit()
            if event.type == k.KEYDOWN:
                if event.key == k.K_DOWN:
                    # to move selection down through the buttons
                    if selected_button == 'start':
                        selected_button = 'controls'
                    elif selected_button == 'quit':
                        selected_button = 'start'
                    elif selected_button == 'controls':
                        selected_button = 'quit'
                elif event.key == k.K_UP:
                    # to move selection up through the buttons
                    if selected_button == 'start':
                        selected_button = 'quit'
                    elif selected_button == 'quit':
                        selected_button = 'controls'
                    elif selected_button == 'controls':
                        selected_button = 'start'
                elif event.key == k.K_RETURN:  # ENTER key
                    if selected_button == 'start':
                        # Start countdown then main game
                        intro = False
                        countdown_screen()
                    elif selected_button == 'quit':
                        quit()
                    elif selected_button == 'controls':
                        controls_screen()
        buttons = {
            'start': {'text': start, 'position': (750, 100)},
            'quit': {'text': quit_button, 'position': (755, 200)},
            'controls': {'text': controls, 'position': (750, 150)}
            }
        
        # Highlight the selected button
        for button_name, button_props in buttons.items():
            if button_name == selected_button:# this part will makke buttons red
                k.draw.rect(screen, (225,0,0), (*button_props['position'], button_props['text'].get_width(), button_props['text'].get_height()), 1)
                button_props['text'] = font2.render(button_name.upper(), True, (225,0,0))
            else: # this will keep rest default black.
                k.draw.rect(screen, (0,0,0), (*button_props['position'], button_props['text'].get_width(), button_props['text'].get_height()), 1)
                button_props['text'] = font2.render(button_name.upper(), True, (0,0,0))

            screen.blit(button_props['text'], button_props['position'])
        k.display.update()

# racing game function:
def main_game_loop():
    k.display.set_caption('Forza Horizon VI')
    track= k.image.load('track(2).png')
    running_game = True
    global obsx 
    global obsy  
    global obsx_change
    global obsy_change
    global obsx2
    global obsy2
    global obsx2_change 
    global obsy2_change 
    global carx
    global cary
    global carx_change
    global cary_change
    global score
    global obs_speed 
    global speed_increment
    paused= False    
    score_board= font.render("Score: 0", True, (255,255,255))
    # adding a constant distance so cars don't move parallely...
    distance_between_cars = obsx2 - obsx

    # setting a constant distance value
    constant_distance = 500  

    # ensuring a constant distance between the obstacle cars
    if distance_between_cars < constant_distance:
        obsx = obsx2 - constant_distance

    if distance_between_cars > constant_distance:
        obsx2 = obsx + constant_distance

    while running_game:

    # track heh heh heh
        screen.blit(track, (0, 0))

        for event in k.event.get():
            if event.type == k.QUIT or (event.type == k.KEYDOWN and event.key == k.K_F4):
                running_game = False
            if event.type == k.KEYDOWN:
                if event.key == k.K_UP:
                    cary_change = -3
                if event.key == k.K_DOWN:
                    cary_change = 3
                if event.key == k.K_RIGHT:
                    carx_change = 3
                if event.key == k.K_LEFT:
                    carx_change = -3
                if event.key == k.K_p: 
                    paused = not paused  # Toggle pause 
                    cary_change = 0
                    carx_change = 0
            if event.type == k.KEYUP:
                if event.key == k.K_LEFT or event.key == k.K_RIGHT:
                    carx_change = 0
                elif event.key == k.K_UP or event.key == k.K_DOWN:
                    cary_change = 0
                

    # Reset the enemy car when it goes off the screen, kinda like restrictions and boundary to enemy cars...
        if obsx < -64: 
            obsx = 1000
        if obsx2< -64:
            obsx2 = 1000
#spawn images of cars at desired locations
        carimg(carx, cary)
        obsimg(obsx, obsy)
        obs2img(obsx2, obsy2)
        if not paused:
            cary += cary_change
            carx += carx_change
            if carx <= 0:
                carx = 0
            if carx >= 250:
                carx = 250
            if cary <= 0:
                cary = 0
            elif cary >= 272:
                cary = 272
            obsx += obsx_change
            obsx2 += obsx2_change

        else:

            pau= font3.render("PAUSED", True, (255,255,200),(0,0,0))
            screen.blit(pau, (335,160))
        collision_obs1 = check_collision(carx, cary, obsx, obsy)
        collision_obs2 = check_collision(carx, cary, obsx2, obsy2)

        if collision_obs1 or collision_obs2:
            paused = True
            #explosion
            explosion= k.image.load('explosion.png')
            explosion_x= (carx + 112)
            explosion_y= (cary + 40)
            screen.blit(explosion, (explosion_x, explosion_y))

            over= font3.render("GAME OVER",True,(255,255,255),(0,0,0))
            screen.blit(over, (310,160))

        else:
            # No collision, increment score if car passes obstacles
            passed_obstacle = False
        if obsx < carx < obsx + 64 or obsx2 < carx < obsx2 + 64:
            passed_obstacle = True

        if passed_obstacle and not previously_passed_obstacle:
            score += 1
            print(score)  #checking score...
            obs_speed += speed_increment
            obsx_change = -obs_speed
            obsx2_change = -obs_speed

        previously_passed_obstacle = passed_obstacle

        score_board= font.render(f"Score: {round(score)}", True, (255,255,255))
        screen.blit(score_board, (20,20))

        k.display.update()

#countdown function:
def countdown_screen():
    n= 3
    for i in range(n, 0, -1):
        cbg= k.image.load('countdown.png')
        screen.blit(cbg, (0,0))
        font4= k.font.Font('f.otf', 200)
        countdown = font4.render(str(i), True,(0,0,0))
        screen.blit(countdown, (445, 130))
        k.display.update()
        time.sleep(1)
    main_game_loop()

#instruction screen
def controls_screen():
    controls = True
    control_bg= k.image.load("instructions.png")
    while controls:
        k.display.set_caption("CONTROLS")
        screen.blit(control_bg, (0,0))

        for event in k.event.get():
            if event.type== k.QUIT:
                controls=False
            if event.type== k.KEYDOWN:
                if event.key== k.K_ESCAPE:
                    controls= False
                    intro_screen()
        k.display.update()
intro= True
game= True
#main loop where what function should be called and which one to close is programmed
while game:
    for event in k.event.get():
        if event.type == k.QUIT:
            quit()

        if intro:
            intro_screen()

        if controls:
            controls_screen()

        elif running_game:
            main_game_loop()
            game= False
        k.display.update()

    k.display.update()