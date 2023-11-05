import pygame
import os
pygame.font.init()
pygame.mixer.init()

FONT = pygame.font.SysFont('comicsans', 40)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_SHOT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3" ))
WINNER_SOUND = pygame.mixer.Sound(os.path.join("Assets","Winnersound.mp3"))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Odyssey")

VEL = 5

FPS = 60

BULLET_VEL = 15
BULLET_AMOUNT = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH,HEIGHT))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

class Movement:
    def movement_red(keys_pressed, red):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and red.x - VEL > 0:
            red.x -= VEL
        if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
            red.x+=VEL
        if keys_pressed[pygame.K_w] and red.y + VEL > 0:
            red.y-=VEL
        if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT:
            red.y+=VEL
        
    def movement_yellow(keys_pressed, yellow):
        if keys_pressed[pygame.K_LEFT] and yellow.x - VEL   > BORDER.x + BORDER.width:
            yellow.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width< WIDTH:
            yellow.x+=VEL
        if keys_pressed[pygame.K_UP] and yellow.y + VEL > 0:
            yellow.y-=VEL
        if keys_pressed[pygame.K_DOWN]  and yellow.y + VEL < HEIGHT:
            yellow.y+=VEL

def bullet_hit(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
    



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #rendring sprites
    WIN.blit(SPACE, (0,0))
    red_health_text = FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = FONT.render(f"Health: {yellow_health}",1,WHITE)
    WIN.blit(red_health_text, (10,10))
    WIN.blit(yellow_health_text, (WIDTH - red_health_text.get_width()-10,10))


    pygame.draw.rect(WIN,WHITE,BORDER)

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        if bullet.x < 0:
            yellow_bullets.remove(bullet)
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = FONT.render(text, 1,RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()

def main():
    
    red = pygame.Rect(100,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700,300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_health = 5
    yellow_health = 5

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(red_bullets) < BULLET_AMOUNT:
                    bullet = pygame.Rect(red.x+red.width, red.y + red.height//2 - 3, 10,5)
                    red_bullets.append(bullet)

                    BULLET_SHOT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < BULLET_AMOUNT:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y + yellow.height//2 - 3, 10,5)
                    yellow_bullets.append(bullet)

                    BULLET_SHOT_SOUND.play()

            if event.type == RED_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()
        if red_health <= 0:
            red_health = 0
            WINNER_SOUND.play()
            draw_winner("Yellow Won!")
        if yellow_health <= 0:
            yellow_health = 0
            WINNER_SOUND.play()
            
            draw_winner("Red Won!")

        keys_pressed = pygame.key.get_pressed()
        Movement.movement_yellow(keys_pressed, yellow)
        Movement.movement_red(keys_pressed, red)

        WIN.fill((0,0,0))
        bullet_hit(yellow_bullets, red_bullets, yellow, red)
        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    main()
