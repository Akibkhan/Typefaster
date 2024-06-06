import pygame
from pygame import image
from pygame.locals import *
import sys
import time
import random
import mysql.connector 
from mysql.connector import errorcode
from mysql.connector import Error
from pygame.time import Clock

import pygame_textinput


pygame.init()
playername = "Player1"




def Converttupletostr(tup):
        str = ''
        for item in tup:
            str = str + item
        return str  

def button(self,msg,x,y,w,h,ic,ac,action=None):

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac,(x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText,(0,0,0))
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)
white = (255,255,255)

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


class FastTyper:
    def __init__(self):
        self.w=750
        self.h=500
        self.reset=True
        self.active = False
        self.input_text=''

        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 255, 255)
        self.TEXT_C = (255,255,255)
        self.RESULT_C = (255,255,255)
        
        pygame.init()
        programIcon = pygame.image.load('logo.png')
        pygame.display.set_icon(programIcon)
        pygame.display.set_caption('Type Faster')

        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))
        self.licon = pygame.image.load('licon.png')
        self.licon = pygame.transform.scale(self.licon, (self.w,self.h))
        r = ["bg.jpg","1.jpg","2.jpg","3.jpg","4.jpg"]
        self.bg = pygame.image.load("bg/"+str(r[random.randint(0,4)]))
        self.bg = pygame.transform.scale(self.bg, (self.w,self.h))
        self.screen = pygame.display.set_mode((self.w,self.h))
        
        

   
        onimg = pygame.image.load('on.png')
        licon = pygame.image.load('licon.png')
        
        
        pygame.mixer.music.load('main.mp3')
        pygame.mixer.music.play(-1)
        gameDisplay = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Faster')
        clock = pygame.time.Clock()


    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()



    def get_sentence(self):

       
        mycon = mysql.connector.connect(host='localhost',username="root",password="root",database="typefaster")
        mycursor = mycon.cursor()
        mycursor.execute("SELECT Text FROM sentences")

        myresult = mycursor.fetchall()
        sent = []
        for snap in myresult:
            a = Converttupletostr(snap)
            sent.append(a)
        
         
        sentence = random.choice(sent)
        return sentence
    
            
    def show_results(self, screen):
        if(not self.end):
            self.total_time = time.time() - self.time_start
        count = 0
        for i,c in enumerate(self.word):
            try:
                if self.input_text[i] == c:
                    count += 1
            except:
                pass
        self.accuracy = count/len(self.word)*100
        self.wpm = len(self.input_text)*60/(5*self.total_time)
        self.end = True
        print(self.total_time)
        self.results = 'Time:'+str(round(self.total_time)) +" secs Accuracy:"+ str(round(self.accuracy)) + "%" + ' Wpm: ' + str(round(self.wpm))
        #MYSQL ADD
        
        mycon = mysql.connector.connect(host='localhost',username="root",password="root",database="typefaster")
        mycursor = mycon.cursor()
        global playername
        qry = "INSERT INTO LEADERBOARD(Name,Time,Wpm) VALUES(%s,%s,%s)"
        val = (playername,int(self.total_time),int(self.wpm))
        #val = (playername,3,4)
        mycursor.execute(qry,val)
        mycon.commit()
        
        self.time_img = pygame.image.load('icon.png')
        self.time_img = pygame.transform.scale(self.time_img, (150,150))
        screen.blit(self.time_img, (self.w/2-75,self.h-140))
        self.draw_text(screen,"Reset", self.h - 65, 26, (255,255,255))

        self.lbimg =  pygame.image.load('lb.png')
        self.lbimg = pygame.transform.scale(self.lbimg,(120,120))
        screen.blit(self.lbimg, (self.w/2-190,self.h-140))
        self.draw_text(screen,"", self.h - 30, 26, (255,255,255))
        print(self.results)
        pygame.display.update()
    
    
    

    def start(self):
     self.reset_game()
     self.running=True
     while(self.running):
         clock = pygame.time.Clock()
         self.screen.fill((0,0,0), (50,250,650,50))
         pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)
         self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))   
         
         
         

        
         for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if(x>=50 and x<=650 and y>=250 and y<=300):
                    self.active = True
                    self.input_text = ''
                    self.time_start = time.time()
                if(x>=310 and x<=510 and y>=390 and self.end):
                    self.reset_game()
                    x,y = pygame.mouse.get_pos()
                
                if(x>=240 and x<=400 and y>=390 and self.end):
                    self.lb()
                    x,y = pygame.mouse.get_pos()
            


            elif event.type == pygame.KEYDOWN:
                if self.active and not self.end:
                    if event.key == pygame.K_RETURN:
                        print(self.input_text)
                        self.show_results(self.screen)
                        print(self.results)
                        self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)
                        self.end = True

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        try:
                            self.input_text += event.unicode
                        except:
                            pass
            
            clock.tick(60)
         pygame.display.update()
        
         

   
    
   
    
  
    
   

     
     
    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))
        pygame.display.update()
        time.sleep(1)
        self.reset=False
        self.end = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        self.screen.fill((0,0,0))
        r = ["bg.jpg","1.jpg","2.jpg","3.jpg","4.jpg"]
        self.bg = pygame.image.load("bg/"+str(r[random.randint(0,4)]))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)
        self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)
        pygame.display.update()
        
    def text_objects(text, font):
            textSurface = font.render(text, True, (0,0,0))
            return textSurface, textSurface.get_rect()
    def quitgame():
     pygame.quit()
     quit()

    def exi():
     pygame.quit()
     quit()
    def run(self):
        self.screen.blit(self.open_img, (0,0))
        
        
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
      
        input_box = pygame.Rect((self.screen.get_width()/2+10),(self.screen.get_height()/2 - 12), 132, 32)
        color_inactive = pygame.Color('red')
        color_active = pygame.Color('green')
        color = color_inactive
        largeText = pygame.font.SysFont("Arial",32)
        TextSurf, TextRect = text_objects("Enter your name:", largeText,(0,0,0))
        TextRect.center = ((self.screen.get_width()/2-100),(self.screen.get_height()/2))
        self.screen.blit(TextSurf, TextRect)
        
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if input_box.collidepoint(event.pos):
                       
                        active = not active
                    else:
                        active = False
                    
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done=True
                            global playername
                            playername = text
                            FastTyper.start(self)
                            
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            txt_surface = font.render(text, True, color)
           
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
           
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
     
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)
    
    
    
    def lb(self):
        black = (0,0,0)
        white = (255,255,255)
        red = (200,0,0)
        green = (0,200,0)
        bright_red = (255,0,0)
        bright_green = (0,255,0)
        intro = True
        try:
            mySQLconnection = mysql.connector.connect(host='localhost',
                                        database='typefaster',
                                        user='root',
                                        password='root')

            sql_select_Query = "SELECT * FROM LEADERBOARD ORDER BY wpm asc"
            cursor = mySQLconnection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            rc = cursor.rowcount
            print("Total number of rows in student is - ", cursor.rowcount)
            print ("Printing each row's column values i.e.  student record")


            cursor.close()

        except Error as e :
            print ("Error while connecting to MySQL", e)
        finally:
            #closing database connection.
            if(mySQLconnection.is_connected()):
                mySQLconnection.close()
                print("MySQL connection is closed")
        while intro:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                    intro=False
                self.screen.fill(white)
            largeText = pygame.font.SysFont("comicsansms",40)
            TextSurf, TextRect = text_objects("HighScore", largeText,(0,0,0))

            TextRect.center = (100,20)
            self.screen.blit(TextSurf, TextRect)
            print(records)

            font = pygame.font.SysFont("comicsansms", 25)
            text = font.render("Rank         Name          Time(seconds)       Wpm", True, black)
            self.screen.blit(text,(5,50))


            text = font.render("___________________________________________________", True,(0,255,255))
            self.screen.blit(text,(5,50))



            font = pygame.font.SysFont("comicsansms", 25)
            if rc >= 1:
                text = font.render("1               "+str((records[0])[1]) +"                    "+str((records[0])[2])+"                           "+str((records[0])[3]), True, black)
                self.screen.blit(text,(5,80))
            if rc >= 2:
                text = font.render("2               "+str((records[1])[1]) +"                   "+str((records[1])[2])+"                           "+str((records[1])[3]), True, black)
                self.screen.blit(text,(5,110))
            if rc >= 3:
                text = font.render("3               "+str((records[2])[1]) +"                   "+str((records[2])[2])+"                           "+str((records[2])[3]), True, black)
                self.screen.blit(text,(5,140))
            if rc >= 4:
                text = font.render("4               "+str((records[3])[1]) +"                     "+str((records[3])[2])+"                           "+str((records[3])[3]), True, black)
                self.screen.blit(text,(5,170))
            if rc >= 5:
                text = font.render("5               "+str((records[4])[1]) +"                   "+str((records[4])[2])+"                           "+str((records[4])[3]), True, black)
                self.screen.blit(text,(5,200))
            if rc >= 6:
                text = font.render("6               "+str((records[5])[1]) +"                   "+str((records[5])[2])+"                           "+str((records[5])[3]), True, black)
                self.screen.blit(text,(5,230))
            if rc >= 7:
                text = font.render("7               "+str((records[6])[1]) +"                   "+str((records[6])[2])+"                           "+str((records[6])[3]), True, black)
                self.screen.blit(text,(5,260))
            if rc >= 8:
                text = font.render("8               "+str((records[7])[1]) +"                   "+str((records[7])[2])+"                           "+str((records[7])[3]), True, black)
                self.screen.blit(text,(5,290))
            if rc >= 9:
                text = font.render("9               "+str((records[8])[1]) +"                   "+str((records[8])[2])+"                           "+str((records[8])[3]), True, black)
                self.screen.blit(text,(5,320))
            if rc >= 10: 
                text = font.render("10              "+str((records[9])[1]) +"                  "+str((records[9])[2])+"                           "+str((records[9])[3]), True, black)
                self.screen.blit(text,(5,350))


            button(self,"Replay!",150,450,100,50,green,bright_green,self.start)
            button(self,"Quit",550,450,100,50,red,bright_red,self.quitgame)
           
            pygame.display.update()
               
k = FastTyper().lb()    


    
