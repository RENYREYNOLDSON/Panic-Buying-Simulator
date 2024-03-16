
import pygame,sys,random,math
from pygame.locals import*

pygame.init()

infoObject=pygame.display.Info()
screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("Panic Buying System")
clock=pygame.time.Clock()

#Fonts
font1=pygame.font.Font('TravelingTypewriter.ttf', 60)


#Images
waterImage=pygame.image.load("water.png").convert_alpha()
foodImage=pygame.image.load("food.png").convert_alpha()
hygieneImage=pygame.image.load("hygiene.png").convert_alpha()

shopColour=(38,51,63)
shopFloorColour=(101,172,233)
tableColour=(154,133,77)

#Variables
day=1
timeCounter=0
panic=0
waterArray=[True,True,True,True,True,True,True,True,True,True]
foodArray=[True,True,True,True,True,True,True,True,True,True]
hygieneArray=[True,True,True,True,True,True,True,True,True,True]
doorPosition=0

class Shopper:
    def __init__(self,x,y,colour,number):
        self.colour=colour
        self.x=x
        self.y=y
        self.number=number
        self.water=random.randint(3,5)
        self.food=random.randint(3,5)
        self.hygiene=random.randint(3,5)
        self.panic=0
        self.stage="home"#Stages are walking,outside,shopping,food,water,hygiene
        self.shopped=False

        
        
    def draw(self):
        pygame.draw.rect(screen,self.colour,(self.x,self.y,20,40),0)

        if self.panic<10:
            pygame.draw.circle(screen,(255,255,255),(self.x,self.y+10),8,0)
            pygame.draw.circle(screen,(255,255,255),(self.x+20,self.y+10),8,0)
        else:
            pygame.draw.circle(screen,(255,0,0),(self.x,self.y+10),8,0)
            pygame.draw.circle(screen,(255,0,0),(self.x+20,self.y+10),8,0)

            
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y+10),4,0)
        pygame.draw.circle(screen,(0,0,0),(self.x+20,self.y+10),4,0)

        if self.food>0:
            pygame.draw.rect(screen,(255,0,0),(self.x-1,self.y-5-self.food*5,4,self.food*5),0)#Draw Stats
        if self.water>0:
            pygame.draw.rect(screen,(0,171,255),(self.x+8,self.y-5-self.water*5,4,self.water*5),0)
        if self.hygiene>0:
            pygame.draw.rect(screen,(255,255,255),(self.x+17,self.y-5-self.hygiene*5,4,self.hygiene*5),0)



    def move(self):
        global foodArray,waterArray,hygieneArray
        if self.stage=="home" and (self.food<3+self.panic or self.water<3+self.panic or self.hygiene<3+self.panic) and self.shopped==False:
            self.stage="walking"
            self.shopped=True

        elif self.stage=="walking":
            if self.x>755 and self.x<775:
                self.stage="outside"
            if self.x<765:
                self.x+=2
            elif self.x>765:
                self.x-=2


            if self.y>700:
                self.y-=2
            elif self.y<700:
                self.y+=2

        elif self.stage=="outside":
            if self.y>400:
                self.y-=2
            else:
                self.stage="choice"

        elif self.stage=="leaving":
            if self.x>760 and self.x<780:
                self.stage="downward"
            if self.x<765:
                self.x+=2
            elif self.x>765:
                self.x-=2

            if self.y>500:
                self.y-=2
            elif self.y<500:
                self.y+=2

        elif self.stage=="downward":
            if self.y<700:
                self.y+=2
            else:
                self.stage="gone"

        elif self.stage=="gone":
            if self.x==40+(self.number-1)*60 and self.y==840:
                self.stage="home"
            if self.x<40+(self.number-1)*60:
                self.x+=2
            elif self.x>40+(self.number-1)*60:
                self.x-=2


            if self.y<840:
                self.y+=2

                
        elif self.stage=="choice":
                if self.food<3+self.panic:
                    self.stage="food"
                elif self.water<3+self.panic:
                    self.stage="water"
                elif self.hygiene<3+self.panic:
                    self.stage="hygiene"
                else:
                    self.stage="leaving"
                    
        elif self.stage=="food":
            count=0
            for i in foodArray:
                if i==True:
                    if self.x>490:
                        self.x-=2
                    if self.y>180+count*35-20 and self.y<180+count*35+20 and self.x<=490:
                        foodArray[count]=False
                        self.food+=1
                        self.stage="choice"
                        if self.panic>0:
                            self.panic-=1
                    elif self.y<180+count*35:
                        self.y+=2
                    elif self.y>180+count*35:
                        self.y-=2
                    return
                count+=1
            if self.water<3+self.panic:
                self.stage="water"
            elif self.hygiene<3+self.panic:
                self.stage="hygiene"
            else:
                self.stage="leaving"
            self.panic+=1


        elif self.stage=="water":
            count=0
            for i in waterArray:
                if i==True:
                    if self.x<1020:
                        self.x+=2
                    if self.y>180+count*35-20 and self.y<180+count*35+20 and self.x>=1020:
                        waterArray[count]=False
                        self.water+=1
                        self.stage="choice"
                        if self.panic>0:
                            self.panic-=1
                    elif self.y<180+count*35:
                        self.y+=2
                    elif self.y>180+count*35:
                        self.y-=2
                    return
                count+=1
            if self.hygiene<3+self.panic:
                self.stage="hygiene"
            else:
                self.stage="leaving"
            self.panic+=1

        elif self.stage=="hygiene":
            count=0
            for i in hygieneArray:
                if i==True:
                    if self.y>230:
                        self.y-=2
                    if self.x>600+count*35-20 and self.x<600+count*35+20 and self.y<=230:
                        hygieneArray[count]=False
                        self.hygiene+=1
                        self.stage="choice"
                        if self.panic>0:
                            self.panic-=1
                    elif self.x<600+count*35:
                        self.x+=2
                    elif self.x>600+count*35:
                        self.x-=2
                    return
                count+=1
            self.stage="leaving"
            self.panic+=1

                    
        

                

def drawShop():
    pygame.draw.rect(screen,shopFloorColour,(400,100,750,510),0)

    #Shadows
    pygame.draw.rect(screen,(7,62,111),(380,100,20,520),0)
    pygame.draw.rect(screen,(7,62,111),(380,80,770,20),0)
    
    
    pygame.draw.rect(screen,shopColour,(400,600,350,20),0)#Bottom Walls
    pygame.draw.rect(screen,shopColour,(800,600,350,20),0)

    pygame.draw.rect(screen,shopColour,(400,100,20,500),0)#Side Walls
    pygame.draw.rect(screen,shopColour,(1130,100,20,500),0)

    pygame.draw.rect(screen,shopColour,(400,100,750,20),0)#Top Wall

    #Shop Shelfs

    #Food
    pygame.draw.rect(screen,tableColour,(440,180,40,360),0)
    pygame.draw.rect(screen,tableColour,(445,540,5,10),0)
    pygame.draw.rect(screen,tableColour,(470,540,5,10),0) 
    #Water
    pygame.draw.rect(screen,tableColour,(1070,180,40,360),0)
    pygame.draw.rect(screen,tableColour,(1075,540,5,10),0)
    pygame.draw.rect(screen,tableColour,(1100,540,5,10),0)

    
    #Hygeine Products
    pygame.draw.rect(screen,tableColour,(600,140,350,40),0)
    pygame.draw.rect(screen,tableColour,(610,180,5,10),0)
    pygame.draw.rect(screen,tableColour,(935,180,5,10),0)

def showDayInfo():
    text=font1.render("Day "+str(day),True,(255,255,255))
    screen.blit(text,(100,50))

    text=font1.render("Panic "+str(panic),True,(255,255,255))
    screen.blit(text,(70,150))
    
def drawShoppers():
    for i in shoppers:
        i.draw()
        i.move()

def drawDoor():
    global doorPosition
    pygame.draw.rect(screen,(50,50,50),(750-doorPosition,605,25,10),0)#Draws the sliding doors
    
    pygame.draw.rect(screen,(50,50,50),(775+doorPosition,605,25,10),0)

    for i in shoppers:
        if i.y<700 and i.y>500 and i.x>700 and i.x<850:
            if doorPosition<25:
                doorPosition+=2
                return
    if doorPosition>0:
        doorPosition-=2

def drawProducts():
    count=0
    for i in waterArray:
        if i==True:
            screen.blit(waterImage,(1070,180+count*35))
        count+=1

    count=0
    for i in foodArray:
        if i==True:
            screen.blit(foodImage,(440,180+count*35))
        count+=1

    count=0
    for i in hygieneArray:
        if i==True:
            screen.blit(hygieneImage,(600+count*35,140))
        count+=1


def nextDay():
    global waterArray,foodArray,hygieneArray,panic
    for i in shoppers:
        if i.water>0:
            i.water-=random.uniform(0.2,0.8)
        if i.food>0:
            i.food-=random.uniform(0.2,0.8)
        if i.hygiene>0:
            i.hygiene-=random.uniform(0.2,0.8)
        i.shopped=False

    waterArray=[True,True,True,True,True,True,True,True,True,True]
    foodArray=[True,True,True,True,True,True,True,True,True,True]
    hygieneArray=[True,True,True,True,True,True,True,True,True,True]


    total=0
    for i in shoppers:
        total+=i.panic

    panic=int(total/26)

    


shoppers=[]
for i in range(26):
    shoppers.append(Shopper(40+i*60,840,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),i+1))

#example=Shopper(40,840,(20,20,20),1)
shoppers[10].panic=50
while True:
    screen.fill((17,72,121))

    timeCounter+=1
    
    drawShop()
    drawDoor()
    drawProducts()
    drawShoppers()
    showDayInfo()

    if timeCounter>=1400:
        nextDay()
        day+=1
        timeCounter=0

    
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)

#In the video: show a single creature buy and sustain himself
#Then explain the panic mechanic
#Then introduce all of the shoppers and run
#Then run with one member being very panicked to show how the panic spreads and items are distribute unfairly. high standard deviation


#Show how to lower panic: use less, dont get as worried

#Then maybe graph certian properties such as panic and resources

#Then explain why panic buying is harmful


#MAKE SHOPPERS ONLY GO ONCE A DAY







    





    
