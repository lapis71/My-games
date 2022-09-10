 #*Make own shooter!

from pygame import *
from random import randint,choice
from time import time as timer

#!clases:
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.SImage = image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def Update(self):
        keys_presed = key.get_pressed()
        speed = 105
    #*Need to make controls
        if keys_presed[K_UP] and self.rect.y >5 :
            self.rect.y -= self.speed
        if keys_presed[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
        if keys_presed[K_LEFT] and self.rect.x >5 :
            self.rect.x -= self.speed
        if keys_presed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
            #print('sa')
    def Fire(self):
        Bullet = Bullets(img_bullet, self.rect.centerx, self.rect.top, (15,20,-15) )
        bullets.add(Bullet)
    def Ulta(self):
        Beam = Bullets(img_Ubeam,self.rect.x,self.rect.top, (15,20,-15) )

class Bullets(GameSprite):
    def update(self):
        speed = 10
        self.rect.y -= speed
        if self.rect.y == 0:
            self.kill()

#class UltraAttack(Player):
 #   def update(self):

class Enemy(GameSprite):
    direction = 'left'
    global lost
    def update(self):
        global lost
        keys = key.get_pressed()
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1
        if lost == 10:
            game = False

#todo Create game window
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Super bio weapon!")
#*Create fone
background = transform.scale(image.load('fone1.png'),(700,500))
mixer.init()
mixer.music.load("density-time-you-cant-fail.mp3")
mixer.music.play()
#//? game variable and flags
life = 5
lost = 0
score = 0
numshot = 5
life = 3
ulta = 5
AktivUlta = 1
reltime = False
warb = 'warbird.png'
warbU = 'warbirdULTA.png'
m1z = 'moskall1z.png'
m1v = 'moskall1v.png'


font.init()
font1 = font.SysFont("Arial",70)
font2 = font.SysFont('Arial',36)
uwin = font1.render("You win!",1,(55,255,55))
ulose = font1.render("You lose!",1,(255,0,0))
pressR = font2.render("Press'F' to restart",1,(255,255,255))

#make sprites(Pov:steal my code:)x3 )
Player = Player(warb,50,400,10)
monsters = sprite.Group()
for i in range(1,6):
    enemy1 = Enemy(m1z,randint(50,600),10,randint(1,3))
    monsters.add(enemy1)
img_bullet = ('buller.png')
img_Ubeam = ('ultraattack.png')
bullets = sprite.Group()
asteroid = sprite.Group()
#for i in range(1,3):
 #   enemy2 = Enemy('asteroid.png',randint(50,600),10,randint(1,3))
 #   asteroid.add(enemy2)

#todo other flags:
game = True
finish = False
clock = time.Clock()
FpS = 60

#todo function for main cycle
def load_sprites():
    Player.reset()
    Player.Update()
    monsters.update()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)

def reoladcheck():
    global reltime
    global window
    global numshot
    if reltime == True:
        now_time = timer()

        if now_time - last_time < 3:
            reolads = font2.render('Reolading, please wait...',1,(150,0,0))
            window.blit(reolads, (260,460))
        elif now_time - last_time >= 3:
            numshot += 5
            reltime = False
    # //?  MAIN CYCLE!
while game:
    window.blit(background,(0,0))
    if not finish:
        load_sprites()

        reoladcheck()

        text_lose = font2.render("Miss: " +str(lost),1,(255,255,255))
        window.blit(text_lose,(10,20))
        text_score = font2.render("Score: " +str(score),1,(255,255,255))
        window.blit(text_score,(10,50))
        text_score = font2.render("Ammo: " +str(numshot),1,(255,255,255))
        window.blit(text_score,(10,80))
        #text_score = font2.render("Зарядка Улт.Атк.: " +str(ulta),1,(255,255,255))
        #window.blit(text_score,(10,110))
        #text_score = font2.render("Улт.Атк.: " +str(AktivUlta),1,(255,255,255))
        #window.blit(text_score,(10,140))
        text_lifes = font2.render('Lifes: ' +str(life),1,(255,255,255))
        window.blit(text_lifes,(win_width - 120,20))
        


    #todo Collides:
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            enemy1 = Enemy(m1z,randint(80,win_width - 80),-40,randint(1,3))
            monsters.add(enemy1)
            ulta -= 1
            if ulta <= 0:
                AktivUlta += 1
                ulta = 5
        if sprite.spritecollide(Player,monsters, False):
            sprite.spritecollide(Player,monsters, True)
            enemy1 = Enemy(m1z,randint(80,win_width - 80),-40,randint(1,3))
            monsters.add(enemy1)
            life -= 1





    # TODO lost and win
    if lost == 10 or life <= 0:
        finish = True
        window.blit(ulose,(win_width / 3,win_height / 2))
        window.blit(pressR,(win_width/2,win_height-100))
    if score == 15:
        window.blit(uwin,(win_width / 3,win_height / 2))
        window.blit(pressR,(win_width/2,win_height-100))
        finish = True

    # TODO other keybinds
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            game = False
        if keys[K_r]:
            numshot = 5
        if keys[K_f]:
            if finish == True:
                finish = False
                lost = 0
                score = 0
                AktivUlta = 1
                ulta = 5
                life = 5

        if keys[K_SPACE]:
            if numshot > 0 and reltime == False:
                Player.Fire()
                numshot -= 1
            
            if numshot == 0 and reltime == False:
                last_time = timer()
                reltime = True
      #  if keys[K_r]:
       #     if AktivUlta >= 1:
        #        Player.Ulta()
         #       print('ulta')
          #      AktivUlta -= 1

   # print("dsad") # * I check everything with this command

      # * I loop the cycle  
    display.update()
    clock.tick(FpS)
    