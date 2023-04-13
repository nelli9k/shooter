from pygame import*
from random import randint
from time import time as timer
#фонова музика
'''
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

kick = mixer.Sound("kick.mp3")
'''

#Ініціація шрифтів та написів
font.init()
font2= font.SysFont("Arial", 36)

background = "background.jpg"
hero = "hero.png"
target = "targets.png"
dot = "dot.png"
asteroi = "asteroi.png"
#Лічильники
score = 0
lost = 0
collide = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, sizex, sizey, player_speed):
        #викликаємо конструктор класу(Sprite)
        sprite.Sprite.__init__(self)
        #кожен спрайт повинен зберігати властивість image 
        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.speed = player_speed

        #кожен спрайт повинен зберігати властивість rect - прямокутник в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #метод що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #метод для керівання спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x = self.rect.x + self.speed
        if keys[K_d] and self.rect.x < 600:
            self.rect.x = self.rect.x + self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
    #метод постріл
    def kick(self):
        bullet = Bullet("dot.png", self.rect.centerx, self.rect.top, 35, 50 , -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global lost
        #зникає якщо дійде до кінця єкрана 
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        global score
        self.rect.y = self.rect.y + self.speed
        if self.rect.y < 0:
            self.kill()




window = display.set_mode((700,500))
display.set_caption("Shooter")
background = transform.scale(image.load(background), (700,500))

ship = Player("hero.png", 5, 350, 75, 75, 12)

targets = sprite.Group()
for i in range(1, 6):
    monster = Enemy(target, randint(80, 700 - 80), -40, 75, 65, randint(1, 8))
    targets.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Enemy(asteroi, randint(80, 700 - 80), -40, 75, 65, randint(1, 8))
    asteroids.add(asteroid)

finish = False
run = True
number_fires = 0
reload_time = False

font = font.SysFont("Arial", 70)
win = font.render("You won", True, (255, 215, 0))
lose = font.render("You lost", True, (255, 215, 0))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if number_fires < 5 and reload_time == False:
                    number_fires = number_fires + 1
                    #kick.play()
                    ship.kick()

                if number_fires >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True

    if not finish:
        window.blit(background, (0,0))

        collides2 = sprite.spritecollide(ship, asteroids, True)
        collides = sprite.groupcollide(targets, bullets, True, True)
        collides_sprites = sprite.spritecollide(ship, targets, False)
        if collides2:
            collide = collide - 1
            asteroids.update()
            asteroids.draw(window)
            
        if collides:
            score = score + 1
            monster = Enemy(target, randint(80, 700 - 80), -40, 80, 80, randint(1, 10))
            targets.add(monster)
            targets.update()
            targets.draw(window)

        if reload_time == True:
            time_now = timer()
            if time_now - last_time <=3:
                reload= font2.render("Wait, reload...", 1, (255, 0, 0))
                window.blit(reload, (255, 450))

            elif time_now - last_time >=3:
                number_fires = 0
                reload_time = False
 
        text = font2.render("Рахунок:" + str(score), 1, (97, 238, 82))                   
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущені:" + str(lost), 1, (97, 238, 82))
        window.blit(text_lose, (10, 50))

        text_lifes = font2.render("Життів:"+ str(collide), 1, (97, 238, 82))
        window.blit(text_lifes, (10, 90))

        if score == 10:  
            window.blit(win, (200, 200))
            finish = True

        if lost == 5 or collides_sprites or collide == 0: 
            window.blit(lose, (200, 200))
            finish = True
            
        ship.update()
        ship.reset()
        targets.update()
        targets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        display.update()
    time.delay(50)