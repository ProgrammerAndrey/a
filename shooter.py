from pygame import *
from random import randint

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption('shooter')
background = transform.scale(image.load('image.jpg'), (win_width, win_height))

all_sprites = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)

class GameSprites(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (75, 75))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

class Player(GameSprites):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(GameSprites):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.down_speed = player_speed

    def update(self):
        self.rect.y += self.down_speed
        if self.rect.y > win_height:
            self.rect.y = -75
            self.rect.x = randint(0, win_width - 75)
            global lost
            lost += 1

class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = transform.scale(image.load('barbecue.png'), (10, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -15

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

mixer.init()
mixer.music.load('48bb90af8e1e401.mp3')
mixer.music.play(-1)

player = Player('1.jpg', 310, 415, 5)
all_sprites.add(player)

for i in range(10):
    enemy_speed = randint(1, 3)
    enemy = Enemy('1.jpg', randint(0, win_width - 75), randint(-455, -75), enemy_speed)
    all_sprites.add(enemy)
    monsters.add(enemy)

clock = time.Clock()
FPS = 60

game = True
lost = 0
killed = 0

while game:
    finished = False # Флаг: стала ли игра завершенной в этом кадре?

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            player.shoot()

    if killed < 10 and lost < 5:
        all_sprites.update()

        hits = sprite.groupcollide(monsters, bullets, True, True)
        
        for enemy in hits:
            killed += 1
            new_enemy_speed = randint(1, 3)
            new_enemy = Enemy('1.jpg', randint(0, win_width - 75), -75, new_enemy_speed)
            all_sprites.add(new_enemy)
            monsters.add(new_enemy)
    
    # Проверка условий победы/поражения
    result_text = None

    if killed >= 10:
        result_text = font2.render('YOU WIN!', True, (0, 255, 0))
        finished = True 
    elif lost >= 5:
        result_text = font2.render('YOU LOSE!', True, (255, 0, 0))
        finished = True

    window.blit(background, (0, 0))
    
    if killed < 10 and lost < 5 or finished: 
        all_sprites.draw(window)
    
    window.blit(font1.render(f'Пропущено: ' + str(lost), True, (255, 255, 255)), (10, 10))
    window.blit(font1.render(f'Сбито: ' + str(killed), True, (255, 255, 255)), (10, 40))
    
    if result_text:
        window.blit(result_text, (200, 200))

    display.update()
    clock.tick(FPS)

quit()