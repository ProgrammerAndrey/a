from pygame import *

# Инициализация окна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Догонялки')
background = transform.scale(image.load('1.jpg'), (win_width, win_height))

# Группы спрайтов
all_sprites = sprite.Group()
walls = sprite.Group()

# Класс для всех спрайтов
class GameSprites(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 100))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока
class Player(GameSprites):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Класс врага
class Enemy(GameSprites):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = 'left'

class Prize(GameSprites):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):
        if self.rect.x <= 425:
            self.direction = 'right'
        if self.rect.x > win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# Класс стены
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Музыка
mixer.init()
mixer.music.load('48bb90af8e1e401.mp3')
mixer.music.play()

# Создание объектов
player = Player('1.jpg', 135, 100, 5)
enemy = Enemy('1.jpg', 500, 250, 1.5)
prize = Prize('images (3).jpg', 550, 270, 0)
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(enemy)

# Создание стен лабиринта (пример)
wall1 = Wall(155, 5, 255, 250, 75, 20, 175) 
wall2 = Wall(155, 5, 255, 100, 65, 600, 20)   
wall3 = Wall(155, 5, 255, 100, 85, 20, 300) 
wall4 = Wall(155, 5, 255, 100, 375, 425, 20)  
wall5 = Wall(155, 5, 255, 400, 235, 20, 150) 
wall6 = Wall(155, 5, 255, 400, 225, 150, 20) 

walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)

all_sprites.add(wall1)
all_sprites.add(wall2)
all_sprites.add(wall3)
all_sprites.add(wall4)
all_sprites.add(wall5)
all_sprites.add(wall6)
clock = time.Clock()
FPS = 60

game = True

while game:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False

            if finish != True:
                if sprite.collide_rect(player, final): #в финале будет картинка с координатами об нее будет стукаться игрок и всё gg
                    window.blit(win, (200, 200))
                    finish = True
                    prize.play('final-fantasy-ix-pobedy-sound.mp3')

                    if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall1, wall2, wall3, wall4, wall5, wall6):
                        finish = True
                        losse.play('20031.mp3') # это звук проигрыша в игре добавить как отдельную функцию
    
    # Обновление и отрисовка спрайтов
    all_sprites.update()
    all_sprites.draw(window)
    
    # Отрисовка стен (можно и через draw группы)
    for wall in walls:
        wall.draw_wall()

    display.update()
    clock.tick(FPS)