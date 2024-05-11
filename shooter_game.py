from pygame import *
from random import randint
from time import time as timer
# подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('ТЫ ВЫИГРАЛ!', True, (255, 255, 255))
lose = font1.render('ТЫ ПРОИГРАЛ!', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# нам нужны такие картинки:
img_back = "background.jpg" # фон игры
img_meteor = "asteroid.png" #метеорит
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_magazin = "magazin.png" # магазин для пуль
#img_game-over = "game-over.png" # экран оканчания
 
score = 0 # сбито кораблей
goal = 10 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 3 # проиграли, если пропустили столько
life = 3 # жизни
puli = 25 # пули

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet)

# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# класс для метиорита
class Metior(GameSprite):
    # движение метиорита
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

# класс для магазина(патрон)
class Magazin(GameSprite):
        # движение магазинов
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
       

# класс спрайта-пули   
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
 
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# создание группы спрайтов-метиоров
meteorits = sprite.Group()
for i in range(1, 2):
    meteorit = Enemy(img_meteor, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    meteorits.add(meteorit)

# создание группы спрайтов-патрон
magazins = sprite.Group()
for i in range(1, 3):
    magazin = Magazin(img_magazin, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    magazins.add(magazin)
 
bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна

rel_time = False # отвечает за перзарядку

num_fire = 0 # переменная для подсчета выстрела


while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # счетик выстрелов и не происходит ли перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False: # если игрок сделал 5 выстрелов
                    last_time = timer() # засекаем время когда это произошло
                    rel_time = True # ставим флаг перезарядки
 
  # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 25, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 5, 255))
        window.blit(text_lose, (10, 50))

        text_life = font2.render("Жизни: " + str(life), 1, (255, 15, 255))
        window.blit(text_life, (10, 80))

        text_puli = font2.render("Патроны:  " + str(puli), 1, (255, 25, 255))
        window.blit(text_puli, (10, 110))        

        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        meteorits.update()
        magazins.update()


        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteorits.draw(window)
        magazins.draw(window)

        # перезарядка
        if rel_time == True:
            now_time = timer() # считавыем время 

            if now_time - last_time < 3: # пока не прошло 3 секунды выводи инфу о перезарядки
                relod = font2.render("ПЕРЕЗАРЯДКА", 1, (255, 23, 255))
                window.blit(relod, (260, 460))
            else:
                num_fire = 0 # обнуляем счетик пуль
                rel_time = False # сбрасывает флаг перезарядки 
 
        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # игрок столкнулся с метиоритом
        if sprite.spritecollide(ship, meteorits, False):
            life = life - 1

        # игрок столкнулся с магазином
        if sprite.spritecollide(ship, magazins, False):
            life = life - 1  
            


        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)