import pygame
import time
import random
import math
from pygame import mixer
#---------------------------------------------------

#initialize
pygame.init()
screen = pygame.display.set_mode((900,800))
playerdatabase = {

}
platformdatabase = {
}
stardatabase = {
}
homedatabase = {
}
#Title and Icon
pygame.display.set_caption("Platformer")

textfilelist = ["plattest.txt"]
#---------------------------------------------------
class Platform :
    def __init__(self,platformX,platformY,platformlen,platformImg) :
        self.platformX = platformX
        self.platformlen = platformlen
        self.platformY = platformY
        self.platformImg = platformImg
    def draw(self) :
        img = pygame.image.load(self.platformImg)
        img = pygame.transform.scale(img,(self.platformlen,30))
        screen.blit(img,(self.platformX,self.platformY))
class Player :
    def __init__(self,playerX,playerY,standingOn,playervector,jumpVector,playerImg,databaseid,playerSpeed) :
        self.playerX = playerX
        self.playerY = playerY
        self.standingOn = standingOn
        self.playerSpeed = playerSpeed
        self.jumpVector = jumpVector
        self.playerImg = playerImg
        self.databaseid = databaseid
        self.playervector = playervector
        self.gravityvector = [1,270]
    def action(self) :
        playerdatabase[self.databaseid].gravity()
        playerdatabase[self.databaseid].bounds()
        playerdatabase[self.databaseid].findunderneath()
        playerdatabase[self.databaseid].draw()

    def draw(self) :
        screen.blit(pygame.image.load(self.playerImg),(self.playerX,self.playerY))
        overfont=pygame.font.Font('freesansbold.ttf',64)
        if self.playerY > 800 :
            over_text = overfont.render("GAME OVER",True,(0,0,0))
            screen.blit(over_text,(200,250))
    def bounds(self) :

        if self.playerX >= 880 :
            self.playerX = 880
        elif self.playerX <= 0 :
            self.playerX = 0
        # ------------------------------------------
    def findunderneath(self) :
        boolean = False
        for p in platformdatabase :
            i = platformdatabase[p]
            if self.playerY - 10 < i.platformY and self.playerY + 32 > i.platformY:
                if self.playerX > i.platformX-32 and self.playerX < (i.platformX + i.platformlen) :
                    boolean = True
        if boolean == True :
            self.standingOn = "solid"
        else :
            self.standingOn = "air"
    def gravity(self) :
        if self.standingOn == "air" :

            # ------------------------------------------
            if self.jumpVector[0] > 0 :
                self.playerY -= self.jumpVector[0] - self.gravityvector[0]
                self.jumpVector[0] -= self.gravityvector[0]
            elif self.jumpVector[0] <= 0 :
                self.jumpVector = [0,0]
                if self.gravityvector[0] < 16 :
                    self.gravityvector[0] += self.gravityvector[0]
                self.playerY += self.gravityvector[0]
        elif self.standingOn == "solid" :
            self.gravityvector = [1,270]
            # ------------------------------------------
        if self.playervector[1] == 180 :
            self.playerX -= self.playervector[0]
        if self.playervector[1] == 0 :
            self.playerX += self.playervector[0]


        # ------------------------------------------
        self.playerY -= self.jumpVector[0]
        # ------------------------------------------
class Star :
    def __init__(self,starX,starY,starImg,gotten,databaseid) :
        self.starX = starX
        self.starY = starY
        self.starImg = starImg
        self.gotten = gotten
        self.databaseid = databaseid
    def draw(self) :
        for i in playerdatabase :
            if playerdatabase[i].playerX > self.starX - 15 and playerdatabase[i].playerX < self.starX + 15 :
                if playerdatabase[i].playerY - 10 < self.starY and playerdatabase[i].playerY+ 32 > self.starY :
                    self.gotten = True

            if self.gotten == False :
                img = pygame.image.load(self.starImg)
                screen.blit(img,(self.starX,self.starY))

class Home :
    def __init__(self,homeX,homeY,homeImg,databaseid,open) :
        self.homeX = homeX
        self.homeY = homeY
        self.homeImg = homeImg
        self.databaseid = databaseid
        self.open = open
        self.done = False
    def draw(self) :

        for i in stardatabase :
            if stardatabase[i].gotten == False :
                self.open == False
                break
            else :

                self.open = True

        if self.done == True :
            Level_clear_font =pygame.font.Font('freesansbold.ttf',64)

            donetext = Level_clear_font.render("Level Clear",True,(0,0,0))
            screen.blit(donetext,(200,250))
        else :
            img = pygame.image.load(self.homeImg)
            screen.blit(img,(self.homeX,self.homeY))


            for i in playerdatabase :
                if playerdatabase[i].playerX > self.homeX - 15 and playerdatabase[i].playerX < self.homeX + 15 and playerdatabase[i].playerY - 10 < self.homeY and playerdatabase[i].playerY+ 32 > self.homeY:
                    print("donneee")
                    print(self.open)
                    if self.open == True:
                        self.done = True

class Master :
    def __init__(self,textfilelist) :
        self.textfilelist = textfilelist
    def decipher(self) :
        amountofplat = 0
        amountofstar = 0
        for i in self.textfilelist :
            with open(i,"r") as f :
                for line in f :


                    identifier,info = line.split("-")
                    if identifier == "platform" :
                        x1,y1,len = info.split(",")
                        platformdatabase["platform" + str(amountofplat)] = Platform(int(x1),int(y1),int(len),'minus.png')
                        amountofplat += 1
                    else :
                        x1,y1 = info.split(",")
                        if identifier == "yen" :
                            stardatabase["star" + str(amountofstar)] = Star(int(x1),int(y1),"yen.png",False,("star" + str(amountofstar)))
                            amountofstar += 1

                        elif identifier == "address" :
                            homedatabase["home"] = Home(int(x1),int(y1),"address.png","home",False)

                        elif identifier == "player1Male" :
                            playerdatabase["player1"] = Player(int(x1),int(y1),"air",[0,0],[0,0],"Player1Male.png","player1",10)
    def createobj(self) :
        for i in stardatabase :
            stardatabase[i].draw()
        for i in homedatabase :
            homedatabase[i].draw()
        for i in platformdatabase :
            platformdatabase[i].draw()



a = Master(textfilelist)
a.decipher()




#---------------------------------------------------

running = True
while running :

    #---------------------------------------------------
    #Events loop

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerdatabase["player1"].playervector = [playerdatabase["player1"].playerSpeed, 180]

            if event.key == pygame.K_RIGHT :
                playerdatabase["player1"].playervector = [playerdatabase["player1"].playerSpeed, 0]

            if event.key == pygame.K_UP and playerdatabase['player1'].standingOn == "solid":
                playerdatabase["player1"].jumpVector[0]= 14

        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerdatabase["player1"].playervector = [0, 0]
            if event.key == pygame.K_UP:
                playerdatabase["player1"].jumpVector = [0, 0]
    #---------------------------------------------------
    # Movement?

    #---------------------------------------------------
    #FunctionCall / Always

    screen.fill((52, 235, 76))
    playerdatabase["player1"].action()
    a.createobj()


    pygame.display.update()

    #---------------------------------------------------
