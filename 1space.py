from pygame import *
# import os

import random

# add root dir
# script_dir = os.path.dirname(__file__)
# print("ini direktori awal == ",script_dir)

#background music
mixer.init()
mixer.music.load('y2mate.com - ROBLOX Music  Horror.mp3')
mixer.music.play()

bullet_sound = mixer.Sound('pew.ogg')
death_sound = mixer.Sound('y2mate.com - ROBLOX Oof Sound Effect.mp3')
win_sound = mixer.Sound('y2mate.com - Old victory sound roblox.mp3')

font.init()
font2 = font.Font(None, 36)
win = font2.render("YOU WIN!", 1, (255,255,0))
lose = font2.render("YOU LOSE.", 1, (255,0,0))

# we need these pictures:
img_back = "Grass.jfif" # game background
img_hero = "Character with face (1).png" # character
img_alien = "Character with face (2).png"
img_bullet = "Real Bullet.png"

# tambahkan os
# img_back = os.path.join(script_dir, img_back)
# img_hero = os.path.join(script_dir, img_hero)
# img_alien = os.path.join(script_dir, img_alien)
# img_bullet = os.path.join(script_dir, img_bullet)

score = 0
missed = 0
goal = 50
max_lost = 1

# parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)

        # each sprite must store an image property
        # player_image = os.path.join(script_dir, player_image)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Monster(GameSprite):
    def update(self):
        global missed
        if self.rect.y <= 500:
            self.slide = "down"
        else:
            self.slide = "restart"

        if self.slide == "down":
            self.rect.y += self.speed
        else:
            self.rect.x = random.randint(1,700)
            self.rect.y = 0
            missed += 1

# main player class
class Player(GameSprite):
    # method for controlling the sprite with keyboard arrows
    def update(self):
        
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    def fire(self):
            bullet = Bullet(img_bullet, ship.rect.x + 35, ship.rect.y, 11, 25, 15)
            bullets.add(bullet)
            
  # the "fire" method (use the player's place to create a bullet there)

class Bullet(GameSprite):
    # method for bullets
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

    

# Create the window
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Zombie Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

# create sprites
ship = Player(img_hero, 100, win_height - 100, 90, 100, 10)

# aliens sprite
aliens = sprite.Group()
for i in range (1,9):
    speed_random = random.randint(1,7)
    print("ini iteraksi ke ",i,)
    alien = Monster(img_alien, random.randint(100,600), 0, 90, 60, random.randint(1,4))
    aliens.add(alien)

bullets = sprite.Group()



# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# Main game loop:
run = True # the flag is cleared with the close window button
while run:
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet_sound.play()
                ship.fire()

    if not finish:
        # refresh background 
        window.blit(background,(0,0))

        # producing sprite movements
        ship.update()
        aliens.update()
        bullets.update()

        collides = sprite.groupcollide(aliens,bullets,True,True)

        for c in collides:
            score += 1
            alien = Monster(img_alien, random.randint(100,600), 0, 90, 60, random.randint(1,4))
            aliens.add(alien)

           

        keys = key.get_pressed()

        text = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text,(10, 20))
        text = font2.render("Missed: " + str(missed), 1, (255,255,255))
        window.blit(text,(10, 50))

        ship.reset()
        aliens.draw(window)

        bullets.draw(window)
        if score >= goal:
            window.blit(win, (280, 250))
            finish = True
            win_sound.play()

        if missed >= max_lost or sprite.spritecollide(ship, aliens, False):
            window.blit(lose, (280, 250)) 
            finish = True 
            death_sound.play()

        display.update()
    # the loop runs every 0.05 seconds
    time.delay(50)
