from pygame import *
from random import randint

# Initialize mixer and load sounds
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Initialize fonts
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win_text = font1.render('YOU WIN!', True, (154, 104, 231))
lose_text = font1.render('YOU LOSE!', True, (197, 23, 46))

# Image paths
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

# Game variables
score = 0
lost = 0
max_lost = 3
goal = 10

# Window setup
win_width = 700
win_height = 500
display.set_caption("Shooter - Nadia Maharani")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# Base sprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Player class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


# Enemy class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


# Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


# Create player
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Create groups
monsters = sprite.Group()
for i in range(15):  # Change number of enemies here
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 7))  # 3x speed boost
    monsters.add(monster)

bullets = sprite.Group()

# Game loop
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        # HUD
        text = font2.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Updates
        ship.update()
        monsters.update()
        bullets.update()

        # Draw everything
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Bullet collisions
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            new_monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(3, 7))
            monsters.add(new_monster)

        # Loss or win conditions
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))
        elif score >= goal:
            finish = True
            window.blit(win_text, (200, 200))

        display.update()
    time.delay(50)