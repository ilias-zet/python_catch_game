
import pygame
import random

pygame.init()
running = True 
pygame.display.set_caption("Щасливе мишеня")

currentImg =0
sprites=[] 
gameover = pygame.image.load("game_over.jpg")
gameover = pygame.transform.scale(gameover,(800,600))
bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg,(800,600))
for i in range(0,60):
    sprite = pygame.image.load("cheese/frame_"+str(i)+"_delay-0.02s.gif")
    sprite = pygame.transform.flip(sprite,False,True)
    sprite = pygame.transform.scale(sprite,(120,100))
    sprites.append(sprite) 

#ScoreBoard
highscore = 0 

font = pygame.font.Font('freesansbold.ttf',32)
cheeseImg = pygame.image.load("cheese.png") 

white = (255,255,255)
black = (0,0,0)

def startGame(): 
    screen = pygame.display.set_mode((800,600))
    def showScore(string,value,x,y,color): 
        Text = font.render((string+str(value)),True,color)
        screen.blit(Text,(x,y)) 


    #ScoreBoard
    global highscore
    global font
    scores = 0 
    level = 1
    lives = 5

    #Время
    paused = False 
    clock = pygame.time.Clock() 
    current_time = 0 
    time_point = pygame.time.get_ticks()
    spawn_time = 5 

    global running
    #Игрок
    playerSide = "right"
    playerImg = pygame.image.load("mouse.png")
    playerX = 370
    playerY = 450
    def player(x,y): 
        screen.blit(playerImg,(x,y))


    global cheeseImg
    cheeses = [] 
    cheese = {
        "cheeseX" : random.randint(0,650),
        "cheeseY" : -100
        }
    cheeses.append(cheese)


    def spawnCheese():
        cheeses.append({"cheeseX" : random.randint(0,650),"cheeseY" : -100}) 

    def renderCheese(x,y):
        if currentImg<60:
            global cheeseImg
            screen.blit(sprites[currentImg],(x,y))
    speed = 1 

    #Collision checking
    def isCollision(cheeseX,cheeseY,playerX,playerY):
        cheeseRect = pygame.Rect(cheeseX,cheeseY,80,70)
        playerRect = pygame.Rect(playerX,playerY,120,145)
        return playerRect.colliderect(cheeseRect)

    frame = pygame.time.get_ticks()

    #Игровой цикл
    while running:
        screen.blit(bg,(0,0))
        global currentImg
        current_time = pygame.time.get_ticks()
        if currentImg>=60: 
            currentImg=0
        if current_time - frame >= 30 and not(paused):
            currentImg+=1
            frame = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = false

        #Обработка нажатия клавиш
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                if playerSide == 'right':
                    playerImg = pygame.transform.flip(playerImg,True,False)
                    playerSide = 'left'
                playerX-=2
            elif event.key == pygame.K_RIGHT:
                if playerSide == 'left':
                    playerImg = pygame.transform.flip(playerImg,True,False)
                    playerSide = 'right'
                playerX+=2

        if playerX<=0:
            playerX =0
        elif playerX>=650:
            playerX=650

        #Цикл поведения сыра
        if not(paused):
            if current_time - time_point >= spawn_time*1000: 
                spawnCheese() 
                time_point = pygame.time.get_ticks()
            if len(cheeses)>0:
                for i in range(0,len(cheeses)-1):
                    x = cheeses[i]["cheeseX"]
                    y = cheeses[i]["cheeseY"]
                    renderCheese(x,y)
                    cheeses[i]["cheeseY"]+=0.1*speed
                    if y>600:
                        lives-=1 
                        cheeses.remove(cheeses[i])
                    if isCollision(x,y,playerX,playerY):
                        cheeses.remove(cheeses[i])
                        scores+=1
                        if scores%3==0: 
                            level+=1 
                            if spawn_time>=1.5:
                                spawn_time*=0.8
                            if speed<10: 
                                speed+=1        
                                
        
        if lives<=0: 
            screen.blit(gameover,(0,0))
            pygame.time.delay(30)
            paused = True 
            if scores>highscore: 
                highscore = scores 
            showScore("GAME OVER","",300,250,black) 
            showScore("highscore: ",highscore,300,280,black)
            showScore("press any key to restart","",220,310,black)
            if event.type == pygame.KEYDOWN:
                startGame()
                
        showScore("Scores: ",scores,10,10,white)
        showScore("Level: ",level,10,40,white)
        showScore("Lives: ",lives,10,70,white)
        player(playerX,playerY)
        pygame.display.update()
        clock.tick(300)

startGame()