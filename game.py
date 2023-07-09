import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Creating variables
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
screen_x = 1280
screen_y = 660
screenwin = pygame.display.set_mode((screen_x,screen_y))


# Images
bgstart = pygame.image.load("bgimg1.jpg")
bgstart = pygame.transform.scale(bgstart,(screen_x,screen_y)).convert_alpha()
snkicon = pygame.image.load("snake-png-20.jpg")
snkicon = pygame.transform.scale(snkicon,(300,380)).convert_alpha()
bgend = pygame.image.load("bgimg2.jpg")
bgend = pygame.transform.scale(bgend,(screen_x,screen_y)).convert_alpha()
bgsnk = pygame.image.load("bgimg.jpg")
bgsnk = pygame.transform.scale(bgsnk,(screen_x,screen_y)).convert_alpha()
paubg = pygame.image.load("pausebg.jpeg")
paubg = pygame.transform.scale(paubg,(screen_x,screen_y)).convert_alpha()
icon = pygame.image.load("pauseicon.jpg")
icon = pygame.transform.scale(icon,(300,290)).convert_alpha()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)

def text_screen(text,color,x,y):
    score_text = font.render(text,True,color)
    screenwin.blit(score_text,[x,y])

exit_game = False

pygame.display.set_caption("Snake")
pygame.display.update()

def plot_snk(screenwin,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(screenwin,color,[x,y,snake_size,snake_size])

# Pausing
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

        screenwin.fill(white)
        screenwin.blit(paubg,(0,0))
        screenwin.blit(icon,(470,190))
        text_screen('''PAUSED!!''',black,530,290)
        text_screen('''Press Space Bar to continue.''',black,355,333)
        pygame.display.update()
        clock.tick(40)


def welcome():
    exit_game = False
    pygame.mixer.music.load("game.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        screenwin.fill((243,180,209))
        screenwin.blit(bgstart,(0,0))
        screenwin.blit(snkicon,(430,50))
        text_screen('''Welcome to the Snake Game.''',black,350,450)
        text_screen('''Press Space Bar to play.''',black,395,490)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.unload()
                    gameloop()

        pygame.display.update()
        clock.tick(40)

def gameloop():

    snk_length = 1
    snk_list = []
    score = 0
    food_x = random.randint(200,screen_x/2)
    food_y = random.randint(200,screen_y/2)
    apple = pygame.image.load("apple.jpg")
    apple = pygame.transform.scale(apple,(30,30)).convert_alpha()
    snake_x = 200
    snake_y = 300
    snake_size = 20
    fps = 40
    speed = 5
    exit_game = False
    game_over = False
    velocity_x = 0
    velocity_y =  0


    while not exit_game:
        if game_over:
            screenwin.fill((210,240,230))
            screenwin.blit(bgend,(0,0))
            text_screen('''Game Over!! Press Enter to replay.''',black,320,290)
            text_screen('''Your score is:  ''' + str(score),black,445,333)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        velocity_y = -speed
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = speed
                        velocity_x = 0

                    if event.key == pygame.K_LEFT:
                        velocity_y = 0
                        velocity_x = -speed

                    if event.key == pygame.K_RIGHT:
                        velocity_y = 0
                        velocity_x = speed

                    if event.key == pygame.K_SPACE:
                        pause()

            if abs(snake_x-food_x)<18 and abs(snake_y-food_y)<18:
                score +=8
                snk_length +=6
                pygame.mixer.music.load("food_.wav")
                pygame.mixer.music.play()
                food_x = random.randint(100,screen_x-100)
                food_y = random.randint(100,screen_y-100)

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            screenwin.fill(white)
            screenwin.blit(bgsnk,(0,0))
            text_screen("Score: " + str(score),black,5,5)
            plot_snk(screenwin,black,snk_list,snake_size)
            screenwin.blit(apple,(food_x,food_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("corners.wav")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_x or snake_y<0 or snake_y>screen_y:
                game_over = True
                pygame.mixer.music.load("corners.wav")
                pygame.mixer.music.play()

        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome()
