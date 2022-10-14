import numpy as np
import pygame 
import random
import time
# 10 X 20 grid
# ( S Z I O J L T )
# ( 0 1 2 3 4 5 6 ) 

# pygame.font.init()



screen_width =600
screen_height=490

play_width =200
play_height =400
block_size = 20 
top_left_x = (screen_width-play_width)/2
top_left_y = screen_height-play_height-10
pygame.font.init()
pygame.init()
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Tetris')



#shapes
Z = [[(1,0),
      (0,1),
      (1,1),
      (0,2)],
     [(0,0),
      (1,0),
      (1,1),
      (2,1)]]
S = [[(2,0),
      (1,0),
      (1,1),
      (0,1)],
     [(0,0),
      (0,1),
      (1,1),
      (1,2)]]
I = [[(1,0),
      (1,1),
      (1,2),
      (1,3)],
     [(0,1),
      (1,1),
      (2,1),
      (3,1)]]
O = [[(0,0),
      (0,1),
      (1,0),
      (1,1)]] 

J = [[(1, 0), (1, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (2, 0), (1, 1), (1, 2)], [(0, 0), (1, 0), (2, 0), (2, 1)]]
L = [[(2, 0), (2, 1), (1, 2), (2, 2)], [(1, 0), (1, 1), (2, 1), (3, 1)], [(2, 0), (3, 0), (2, 1), (2, 2)], [(1, 0), (2, 0), (3, 0), (3, 1)]]
T = [[(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)]]


shapes= [S  ,Z , I , O , J , L , T]
shape_colors=[(255,200,0) ,(255, 153, 51) ,(255, 0, 0),(0, 51, 204),(0, 204, 255),(0, 153, 51),(0, 255, 0)]
BLACK_COLOR = (0,0,0)
WHITE_COLOR = (255,255,255)
GAME_SCORE = 0
MIN_HEIGHT = 0
HIGH_GAME_SCORE = 0 
RESTART_GAME=False

grid_occupied = np.zeros((20,10))
grid_colors =[[(0,0,0) for _ in range(10)] for  _ in range(20)]



current_piece = None
next_coming_piece = None

class Piece:
    def __init__(self , x, y , index ):
        self.x= x
        self.y= y
        self.color= shape_colors[index]
        self.shape = shapes[index]
        self.rotate =0
def get_random_piece():
    r = random.randint(0,len(shapes)-1)
    return Piece(4,-4 , r)

current_piece = get_random_piece()
next_coming_piece = get_random_piece()



def assign_new_piece():
    global current_piece , next_coming_piece ,RESTART_GAME ,GAME_SCORE ,HIGH_GAME_SCORE ,MIN_HEIGHT
    p = current_piece
    GAME_SCORE+=1
    HIGH_GAME_SCORE =max(HIGH_GAME_SCORE , GAME_SCORE)


    r = current_piece.rotate
    for i in range(4):
        x = p.x+p.shape[r][i][0]
        y = p.y+p.shape[r][i][1]
        MIN_HEIGHT = min(MIN_HEIGHT ,y)
        grid_colors[y][x] =current_piece.color
        grid_occupied[y][x] =1
    if MIN_HEIGHT<0:
            RESTART_GAME = True
            return

    current_piece = next_coming_piece
    next_coming_piece = get_random_piece()

def check_piece_collision(p):
    r = p.rotate
    for i in range(4):
        x = p.x+p.shape[r][i][0]
        y = p.y+p.shape[r][i][1]
        if x<0 or x>9 or y>18:
            return False
        if grid_occupied[y][x]==1:
            return False
    return True
        



def rotate_current_piece(r):
    global current_piece , next_coming_piece

    if r==1:
        current_piece.rotate = (current_piece.rotate+1)%len(current_piece.shape) 
        if not check_piece_collision(current_piece):
            current_piece.rotate = (current_piece.rotate-1)%len(current_piece.shape) 

    
    else:
        current_piece.rotate = (current_piece.rotate-1)%len(current_piece.shape) 
        if not check_piece_collision(current_piece):
            current_piece.rotate = (current_piece.rotate+1)%len(current_piece.shape) 



def destroy_last_row():
    global current_piece , next_coming_piece

    sum=0
    for i in range(0,10):
        sum+=grid_occupied[19][i]
    if sum==10:

        for i in range(19,0,-1):
            for j in range(0,10):
                grid_occupied[i][j] = grid_occupied[i-1][j]
                grid_colors[i][j] = grid_colors[i-1][j]


def piece_sidewards(dir):
    global current_piece , next_coming_piece

    p =current_piece
    r = p.rotate

    if dir==1: 
        for i in range(4):
            x = p.x+p.shape[r][i][0]+1
            y = p.y+p.shape[r][i][1]
           
            if y>=0 and (x>9 or grid_occupied[y][x]==1):
                return
        current_piece.x+=1
    else: 
        for i in range(4):
            x = p.x+p.shape[r][i][0]-1
            y = p.y+p.shape[r][i][1]
            if y>=0 and (x<0 or grid_occupied[y][x]==1):
                return         
        current_piece.x-=1
    




def piece_downwards():
    global current_piece , next_coming_piece

    p =current_piece
    r = p.rotate
    for i in range(4):
        x = p.x+p.shape[r][i][0]
        y = p.y+p.shape[r][i][1]+1
        if y>=0 and (y>18 or grid_occupied[y][x]==1):
            assign_new_piece()
            return
        
    current_piece.y+=1




def draw_board():
    global current_piece , next_coming_piece
    #clear the full window
    gameWindow.fill(WHITE_COLOR)
    #black out the full game space
    for i in range(0,19):
        for j in range(0,10):
            pygame.draw.rect(gameWindow ,grid_colors[i][j] , [top_left_x+j*block_size , top_left_y+i*block_size ,block_size ,block_size])
    #draw the current piece
    for i in range(4):
        p = current_piece
        r = p.rotate
        x = top_left_x+block_size*p.x+block_size*p.shape[r][i][0]
        y = top_left_y+block_size*p.y+block_size*p.shape[r][i][1]
        if p.y+p.shape[r][i][1]>=0:
            pygame.draw.rect(gameWindow , p.color, [x,y , block_size ,block_size])
    #heading the tetris
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render('TETRIS', True, WHITE_COLOR, BLACK_COLOR)
    textRect = text.get_rect()
    textRect.center = (300 ,40 ) 
    gameWindow.blit(text, textRect)

    #drawing the score
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('SCORE', True, shape_colors[2], WHITE_COLOR)
    textRect = text.get_rect()
    textRect.center = (500 ,100 ) 
    gameWindow.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 35)
    text = font.render(str(GAME_SCORE), True, BLACK_COLOR)
    textRect = text.get_rect()
    textRect.center = (500 ,123 ) 
    gameWindow.blit(text, textRect)

    #drawing the highest game score
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render('HIGHSCORE', True, shape_colors[5], WHITE_COLOR)
    textRect = text.get_rect()
    textRect.center = (500 ,150 ) 
    gameWindow.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 35)
    text = font.render(str(HIGH_GAME_SCORE), True, BLACK_COLOR)
    textRect = text.get_rect()
    textRect.center = (500 ,175 ) 
    gameWindow.blit(text, textRect)

    #next coming piece hint draw
    pygame.draw.rect(gameWindow ,(129, 138, 126) ,[420,230,160,150])
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render('NEXT COMING PIECE', True, BLACK_COLOR)
    textRect = text.get_rect()
    textRect.center = (500 ,250 ) 
    gameWindow.blit(text, textRect)

    for i in range(4):
        p = next_coming_piece

        r = p.rotate
        x = 470+block_size*p.shape[r][i][0]
        y = 280+block_size*p.shape[r][i][1]
        pygame.draw.rect(gameWindow , p.color, [x,y , block_size ,block_size])

    pygame.display.update()





 





def START_GAME(speed):
    global  MIN_HEIGHT  ,GAME_SCORE ,RESTART_GAME,current_piece ,next_coming_piece 
    global grid_colors , grid_occupied 
    grid_occupied = np.zeros((20,10))
    grid_colors =[[(0,0,0) for _ in range(10)] for  _ in range(20)]
    MIN_HEIGHT =20
    GAME_SCORE = 0 
    RESTART_GAME =False
    current_piece = get_random_piece()
    next_coming_piece = get_random_piece()
    while not RESTART_GAME:
        for ev in pygame.event.get():
            
            if ev.type == pygame.QUIT :
                pygame.quit()
                quit()
            if ev.type==pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    piece_sidewards(1)
                if ev.key == pygame.K_LEFT:
                    piece_sidewards(-1)
                if ev.key == pygame.K_UP:
                    rotate_current_piece(1)
                if ev.key == pygame.K_DOWN:
                    rotate_current_piece(-1)
            # print(ev)
        draw_board()

    
        
        time.sleep(speed)
        piece_downwards()
        destroy_last_row()
    
     







RESTART_GAME  =  True
while True:
    if RESTART_GAME:
        START_GAME(.2)


 
pygame.quit()
quit()





 

