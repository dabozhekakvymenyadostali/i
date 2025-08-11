from pygame import *
mixer.init()
font.init()
from random import *
from time import time as timer

mw = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
display.set_caption('Шутер')
clock = time.Clock()
mixer.music.load('space.ogg')
mixer.music.play()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)
count_skip = 0

class GameSprite(sprite.Sprite):
    def __init__(self, image_player, x, y, speed, pixels_x, pixels_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_player), (pixels_x, pixels_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 4, 15, 20))

class Enemy(GameSprite):
    def update(self):
        global count_skip
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5, 620)
            self.speed = randint(1, 2)
            count_skip += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 310, 395, 5, 80, 100)

monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy('ufo.png', randint(5, 620), -50, randint(1, 2), 80, 50))

asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Enemy('asteroid.png', randint(5, 620), -50, randint(1, 2), 80, 50))

bullets = sprite.Group()

game = True
finish = False
score = 0
health = 3
#reload_time = False
#count_bullets = 0
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                '''if count_bullets < 5 and reload_time == False:
                    player.fire()
                    count_bullets += 1
                if count_bullets >= 5 and reload_time == False:
                    reload_time = True
                    start_time = timer()'''

    if not finish:
        mw.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        monsters.draw(mw)
        bullets.draw(mw)
        asteroids.draw(mw)
        label3 = font1.render('Здоровье '+str(health), True, (250, 0, 0))
        mw.blit(label3, (500, 0))
        label = font1.render('Пропущенные тарелки :D '+str(count_skip), True, (250, 250, 250))
        mw.blit(label, (0, 0))
        collide = sprite.groupcollide(asteroids, bullets, False, True)
        collide = sprite.groupcollide(monsters, bullets, True, True)
        #
        for i in collide:
            score += 1
            monsters.add(Enemy('ufo.png', randint(5, 620), -50, randint(1, 2), 80, 50))
        label2 = font1.render('Сбитые тарелки '+ str(score), True, (250, 250, 250))
        mw.blit(label2, (0, 30))
        if sprite.spritecollide(player, monsters, False):
            health -= 1
            sprite.spritecollide(player, monsters, True)
            monsters.add(Enemy('ufo.png', randint(5, 620), -50, randint(1, 2), 80, 50))
        if sprite.spritecollide(player, asteroids, False):
            health -= 1
            sprite.spritecollide(player, asteroids, True)
            asteroids.add(Enemy('asteroid.png', randint(5, 620), -50, randint(1, 2), 80, 50))
        if health == 0 or count_skip >= 7:
            finish = True
            label_lose = font2.render('ВЫ ПРОИГРАЛИ(((((', True, (250, 250, 250))
            mw.blit(background, (0, 0))
            mw.blit(label_lose, (100, 150))
        if score >= 10:
            finish = True
            label_win = font2.render('ВЫ ПОБЕДИЛИ!1!1!!!', True, (250, 250, 250))
            mw.blit(background, (0, 0))
            mw.blit(label_win, (95, 150))
    display.update()
    clock.tick(60)
