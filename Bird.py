from typing import Any
import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 500
fps = 60

black = (0, 0,0)
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)


font = pygame.font.SysFont('Bauhaus 93', 60)


#variables

player_x = 0
player_y = 0

ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
pipe_gap = 150
pipe_freq = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
pass_pipe = False




#load IMages

bg = pygame.image.load('git.png')
gr = pygame.image.load('gr.png')
restart_button = pygame.image.load('restart.png')

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()


def draw_score(text, font, text_col, x, y):

    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0

        for num in range(1,3):
            img = pygame.image.load(f'hd{num}.png').convert_alpha()
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        #velocity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 450:
                self.rect.y += int(self.vel)


        #Jump
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -8
        
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            # Animation
            self.counter += 1
            flap_cooldown = 10

            if self.counter >  flap_cooldown : 
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotation

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # Position : -1 is from bottom, 1 is from top
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2) ]
        


    def update(self):
        
        self.rect.x -= int(scroll_speed)
        if self.rect.x < 0:
            self.kill()

        
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(200, int(HEIGHT / 2))

bird_group.add(flappy)



#Main function Loop
running = True
while running:

    timer.tick(fps)
    screen.fill(black)

    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    screen.blit(gr, (ground_scroll, 450))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_score(str(score), font, white, int(WIDTH / 2), 0)
    






    # check collision

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Checking if Game over:

    if flappy.rect.bottom > 450:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # create pipe
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now




        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 30:
            ground_scroll = 0

        pipe_group.update()

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
       

    pygame.display.update()
    pygame.display.flip()

pygame.Quit()