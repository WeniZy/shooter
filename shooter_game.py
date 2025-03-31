from pygame import *
from random import randint
from time import time as timer
font.init()
mixer.init()

window = display.set_mode((700,500))

display.set_caption('шутер')

background = transform.scale(image.load('galaxy.jpg'),(700,500))

font1 = font.SysFont('Aria',35)
font2 = font.SysFont('Aria',70)
win = font2.render('YOU WIN', True, (0,255,0))
lose = font2.render('YOU LOSE', True, (255,0,0))
clock = time.Clock()
FPS = 120
lost = 0 #счетчик
score = 0 #счетчик
game = True
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 500 - 80:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
        
fire_sound = mixer.Sound('fire.ogg')


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__(player_image, player_x, player_y, w, h, player_speed)
        self.direction = 1  # 1 - вправо, -1 - влево
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.direction * 3  # Скорость по горизонтали
        # Меняем направление при достижении границ экрана
        if self.rect.x <= 0 or self.rect.x >= 700 - self.rect.width:
            self.direction += -1
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(100, 600)
            self.rect.y = 0
            lost += 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

player = Player('rocket.png', 0,400,60,60,6)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0,620), -40,80,50,randint(1,3))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0,620), -40,80,50,randint(1,3))
    monsters.add(monster)

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1) #громкомть 10%
fire = mixer.Sound('fire.ogg')
num_fire = 0
rel_time = False
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    
    if not finish:
        window.blit(background,(0,0))

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('wait, reload', True,(150,0,0))
                window.blit(reload,(250,400))
            else:
                num_fire=0
                rel_time = False


        
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose,(0,0))
        text_score = font1.render('счет:' + str(score), 1, (255,255,255))
        window.blit(text_score,(0,30))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
    
        if sprite.spritecollide(player, monsters, False):
           finish = True
           window.blit(lose, (250,250))

        if lost>10:
            finish = True
            window.blit(lose, (250,250))
        
        if sprite.groupcollide(monsters,bullets, True, True):
            score += 1
            monster = Enemy('ufo.png', randint(0,620), -40,80,50,randint(1,5))
            monsters.add(monster)
    
        if score == 30:
            finish = True
            window.blit(win, (250,250))
    


        sprite.collide_rect(player, monster)
    display.update()
    clock.tick(60)