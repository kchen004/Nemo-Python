#Kyle Chen
#CS179j Embadded System Senior Design
#Prototype1
#nemo.py
#Nemo's dad Marlin trying to swim through jellyfishes
#1/24/07
#
#Learned how to use sprite and many idea from pyg_star_wars.py by Kevin Harris


import sys
import pygame
import random


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480 

LIGHT_BLUE = [128,128,255]


#life and score booster
class pots(pygame.sprite.Sprite):

    imagesets = [
        pygame.image.load("1.png"),
        pygame.image.load("2.png")
    ]

    def __init__( self, type, current_time ):
        pygame.sprite.Sprite.__init__( self )
        self.image = self.imagesets[type]
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, 500)
        self.rect.centery = random.randint(0, 480)
        self.update_time = current_time+10000
        
            
    def update( self, current_time ):
        #after some time, the item is no longer avaliable
        if self.update_time < current_time:
            self.kill()
            self.update_time = current_time + 10000

        #delete the item once it goes out of right side of the screen
        if self.rect.left > 650:
            self.kill()


#the jellyfish
class Jellyfish(pygame.sprite.Sprite):
    
    jfish =pygame.image.load("3.png")
    
    def __init__( self, startx, starty ):
        pygame.sprite.Sprite.__init__( self )
        self.image = self.jfish
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty
        self.x_velocity = random.randint( 10, 15)
        self.y_velocity = random.randint( -3, 3 )
        self.update_time = 0
            
    def update( self, current_time ):
        #update its movement
        if self.update_time < current_time:
            self.rect.move_ip( (self.x_velocity, self.y_velocity) )
            self.update_time = current_time + 60

        #delete the jellyfish once it goes out of the right side of the screen
        if self.rect.left > 650:
            self.kill()
        

#the main charactor and keyboard action
class fMarlin(pygame.sprite.Sprite):

    DIR_IDEL = 0
    DIR_LEFT = 1
    DIR_RIGHT = 2
    DIR_UP = 3
    DIR_DOWN = 4
    
    def __init__(self):
        pygame.sprite.Sprite.__init__( self )
        self._images = {
            'swim1' : pygame.image.load("marlin.png"),
            'scared' : pygame.image.load("marlin2.png") 
        }
        self.image = self._images['swim1']
        self.rect = self.image.get_rect()
        self.rect.centerx = 160
        self.rect.centery = 368
        self.running = 0
        self._direction = fMarlin.DIR_IDEL
        
    def update(self, stats):
        if stats == "SCARED":
            self.image = self._images['scared']
        else:
            self.image = self._images['swim1']      

    #start the game
    def _start(self):
        self.running = 1
        pygame.time.set_timer(EVENT_THINK, 10)
    
    #pause the game
    def _stop(self):
        self.running = 0
        pygame.time.set_timer(EVENT_THINK, 0)


    #return the running variable
    def isrunning(self):    
        if self.running == 1:
            return 1
        else:
            return 0
    
    #where to go according to the state
    #and keep Marlin inside the screen
    def think(self):
        if self._direction == fMarlin.DIR_RIGHT:
            self.rect.move_ip( (3, 0) )
        elif self._direction == fMarlin.DIR_LEFT:
            self.rect.move_ip( (-3, 0) )
        elif self._direction == fMarlin.DIR_UP:
            self.rect.move_ip( (0, -3))         
        elif self._direction == fMarlin.DIR_DOWN:
            self.rect.move_ip( (0, 3))

        #keep player inside the screen
        if self.rect.right > 640:
            self.rect.move_ip( (-3, 0) )
        elif self.rect.left < 0:
            self.rect.move_ip( (3, 0) )
        elif self.rect.bottom > 480:
            self.rect.move_ip( (0, -3)) 
        elif self.rect.top < 0:
            self.rect.move_ip( (0, 3))
    
    
    #when a key is pressed, set the state
    def processKeyPress(self, key):
        if not self.running:
            if key == pygame.K_s:
                self._start()
        elif self.running:
            if key == pygame.K_LEFT:
                self._direction = fMarlin.DIR_LEFT
            elif key == pygame.K_RIGHT:
                self._direction = fMarlin.DIR_RIGHT
            elif key == pygame.K_UP:
                self._direction = fMarlin.DIR_UP
            elif key == pygame.K_DOWN:
                self._direction = fMarlin.DIR_DOWN
            elif key == pygame.K_s:
                self._stop()

    #when key is released, set the state
    def processKeyRelease(self, key):
        if self.running:
            self._direction = fMarlin.DIR_IDEL


            
EVENT_THINK = pygame.USEREVENT




def main():
    pygame.init()


    #create the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    background = pygame.image.load("ocean.png")
    screen.blit(background, (0,0))
    pygame.display.set_caption( "Finding Nemo" )
    my_font = pygame.font.SysFont("Verdana", 16)
    my_font2 = pygame.font.SysFont("Verdana", 32)   

    screenoffset1 = 0
    screenoffset2 = -640

    #initialize Marlin
    Marlin = fMarlin()  
    MarlinSprite = pygame.sprite.RenderClear()
    MarlinSprite.add(Marlin)
    MarlinStats = "SWIM"
    
    #initialize items
    heart = pygame.sprite.RenderClear()
    point = pygame.sprite.RenderClear()
    potFreqCounter = 0

    #initialize scoring
    blood = 100
    score = 1000
    score_time = 0
    
    #initialize Jellyfish, with two in the beginning
    jellySprites = pygame.sprite.RenderClear()
    jellySprites.add(Jellyfish(100, 0))
    jellySprites.add(Jellyfish(50, 680))
    
    #count time in between jellyfish appear
    jellyFreqCounter = 0


    while 1:
        for event in pygame.event.get():
            #when a key is pressed
            if event.type == pygame.KEYDOWN:
                if((event.key == pygame.K_ESCAPE)
                or(event.key == pygame.K_q)):
                    sys.exit()
                else:
                    Marlin.processKeyPress(event.key)
            #when keys are released
            elif event.type == pygame.KEYUP:
                Marlin.processKeyRelease(event.key)
            elif event.type == pygame.USEREVENT:
            
                Marlin.think()
        #get the running variable
        running = Marlin.isrunning()
        
        #game is paused
        if not running:
            screen.blit(my_font.render("Press \"s\" to start or \"q\" to quit", True, [0,0,0]), [225,20])

        #game is running        
        elif running:
    
            #add more jellyfish
            jellyFreqCounter += 1
            if jellyFreqCounter >= 100:
                jellySprites.add(Jellyfish(random.randint(0, 450),  -500))
                jellySprites.add(Jellyfish(random.randint(0, 450), 980))
                jellySprites.add(Jellyfish(-300, random.randint(0, 480)))
                jellySprites.add(Jellyfish(-300, random.randint(0, 480)))
                jellyFreqCounter = 0
            
    
            #add rescources
            potFreqCounter += 1
            if potFreqCounter >= 100:
                choice = random.randint(0,1)
                if choice == 0:
                    heart.add(pots(0, current_time));
                else:
                    point.add(pots(1, current_time));
                potFreqCounter = 0

            #update the time            
            current_time = pygame.time.get_ticks()

            #update score and blood
            if score_time < current_time:
                score_time = current_time + 30
                score += 1
                
                
                #collision detection
                MarlinStats = "SWIM"
                for collision in pygame.sprite.groupcollide(jellySprites, MarlinSprite, 0, 0):
                    blood -= 0.3
                    score -= 1
                    #make Marlin look scared when get hit
                    MarlinStats = "SCARED"
                    
                for collision in pygame.sprite.groupcollide(heart, MarlinSprite, 1, 0):
                    blood += 20
                for collision in pygame.sprite.groupcollide(point, MarlinSprite, 1, 0):
                    score += 100

            #update all 
            jellySprites.update(current_time)
            MarlinSprite.update(MarlinStats)
            heart.update(current_time)
            point.update(current_time)
            
            #redraw everything
                
            #make the background look continuous and moving
            if screenoffset1 > 640:
                screenoffset1 = -640
            if screenoffset2 > 640:
                screenoffset2 = -640
            screenoffset1 += 1
            screenoffset2 += 1
            screen.blit(background, (screenoffset1,0))
            screen.blit(background, (screenoffset2,0))

            #draw jellyfish, Marlin, and items
            jellySprites.draw(screen)
            MarlinSprite.draw(screen)           
            heart.draw(screen)
            point.draw(screen)

            #display the scoring and life
            hp = str(blood)
            score_s = str(score)
            screen.blit(my_font.render("Life: "+ hp, True, [255,0, 0]), [550,440])
            screen.blit(my_font.render("Score: " + score_s, True, [0,255,255]), [10, 440])
            
        #check if gameover
        if blood < 0:
            score_s = str(score)
            screen.blit(my_font2.render("GAMEOVER", True, [255,0,0]), [225, 50])
            screen.blit(my_font2.render(score_s, True, [0,0,0]), [250, 100])
            Marlin._stop()
        
        
    
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
