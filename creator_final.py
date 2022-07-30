import pygame
import time
import random
import math
from pygame import mixer


pygame.init()
screen = pygame.display.set_mode((900,800))

#Title and Icon
pygame.display.set_caption("Platformer")
# ---------------------------------------------------------
database = {
}
with open("plattest.txt", "r+") as f :
    f.truncate()
# ---------------------------------------------------------
class button():
    def __init__(self, color, x,y,width,height, text='',img=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.img = img
        self.imglist = ['minus.png','yen.png','address.png','player1Male.png']
        self.actingimg = "minus.png"

    def draw(self,screen,outline=None):
        #Call this method to draw the button on the screen

        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 32)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        if self.img != False :
            img = pygame.image.load(self.actingimg)
            img = pygame.transform.scale(img,(30,30))
            screen.blit(img,(self.x + (self.width/2 - 15 ),self.y + (self.height - 30)))

    def switch(self) :
        if self.imglist[-1] != self.actingimg :
            x = self.imglist[self.imglist.index(self.actingimg) + 1]
        else :
            x = self.imglist[0]
        self.actingimg = x



class Platform :
    def __init__(self,xpos,ypos,len) :
        self.xpos = int(xpos)
        self.ypos = int(ypos)
        self.len = int(len)
    def draw(self) :
        img = pygame.image.load('minus.png')
        img = pygame.transform.scale(img,(self.len,30))
        screen.blit(img,(self.xpos,self.ypos))
class Special :
    def __init__(self,specialX,specialY,img) :
        self.specialX = specialX
        self.specialY = specialY
        self.img = img
    def draw(self) :
        img = pygame.image.load(self.img)
        screen.blit(img,(self.specialX,self.specialY))

def addtofile(xval,yval,identifier,len="") :
    with open("plattest.txt", "a") as f :
        if len != "" :
            f.write(identifier + "-" + str(xval)+","+str(yval)+","+str(len) + '\n')
        else :
            f.write(identifier + "-" + str(xval)+","+str(yval)+ '\n')
def drawcommits() :
    font = pygame.font.SysFont('comicsans', 32)
    text = font.render("Commits : " + str(amountcommit), 1, (0,0,0))
    screen.blit(text,(750,35))
# ---------------------------------------------------------
yes = button((225,5,225),30,720,80,80,"Commit?")
no = button((225,225,5), 130,720,80,80,"No?")
select = button((5,225,225), 230,720,80,80,"Selected",True)
running = True
nopressed = False
button = False
amountcommit = 0
while running :

    #---------------------------------------------------
    #Events loop
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos


                # gives you the point you clicked
                if mouse_x < yes.x + yes.width and mouse_x > yes.x and mouse_y < yes.y + yes.height and mouse_y > yes.y :
                    #you pressed in the bounds of the Yes button
                    button = "Yes"

                elif mouse_x < no.x + no.width and mouse_x > no.x and mouse_y < no.y + no.height and mouse_y > no.y :
                    #you pressed in the bounds of the No button
                    button = "No"
                    pass
                elif mouse_x < select.x + select.width and mouse_x > select.x and mouse_y < select.y + select.height and mouse_y > select.y :
                    #you pressed in the bounds of the No button
                    button = "Select"
                    pass
                else :
                    button = "False"
                    if select.actingimg == "minus.png" :
                        firsthalf = str(mouse_x) + "," + str(mouse_y) + ","

                #first half is the original x and y
                print(button)
                print(database)
        elif event.type == pygame.MOUSEBUTTONUP:
            if button == 'False':
                mouse_x2, mouse_y2 = event.pos

                if select.actingimg == "minus.png" :
                    secondhalf = str(int(math.fabs(mouse_x - mouse_x2)))
                    database["platform" + "-" + str(mouse_x2) + str(mouse_y2)] = Platform(mouse_x,mouse_y,secondhalf)
                else :
                    a = select.actingimg[:-4]
                    database[a + "-" + str(mouse_x2) + str(mouse_y2)] = Special(mouse_x,mouse_y,select.actingimg)


            elif button == "Select" :
                select.switch()
            else:

                    if button == "No" :
                        if len(database) > 0 :
                            listofkeys = list(database.keys())

                            database.pop(listofkeys[-1])

                    elif button == "Yes" :
                        for i in database :
                            identifier,garbage = i.split("-")
                            if identifier == "platform" :
                                addtofile(database[i].xpos, database[i].ypos,identifier,database[i].len)
                            else :
                                addtofile(database[i].specialX,database[i].specialY,identifier)

                        amountcommit += 1





    screen.fill((225,225,225))

    for i in database :
        database[i].draw()

    yes.draw(screen)
    no.draw(screen)
    select.draw(screen)
    drawcommits()

    pygame.display.update()
