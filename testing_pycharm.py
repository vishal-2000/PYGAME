# lets start pyGAMING
import pygame

pygame.init()

win = pygame.display.set_mode((640, 640))
pygame.display.set_caption("River Crossing")

# ********************************************* GLOBAL VARIABLES ******************************************************

w_width = 640
w_height = 640
level = 0
# score = 0
# score_2 = 0
score = [0, 0, 0]  # here score[1] represents player 1, score[2] represents player 2
player_no = 1  # reports player no. ----- player_1 = 1, player_2 = 2

# *********************************************** Sounds **************************************************************

winSound = pygame.mixer.Sound('winn.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('main_music.mp3')
pygame.mixer.music.play(-1)

# *********************************************** Images **************************************************************

bg = pygame.image.load('water.jpg')
char = pygame.image.load('ball.png')
char_2 = pygame.image.load('ship.png')
char_3 = pygame.image.load('tornado.png')

# ************************************************ Clock Time *********************************************************
clock = pygame.time.Clock()


# ***************************************** Players *******************************************************************
class PLAYER(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x, self.y, 64, 64)

    def draw(self, win):
        win.blit(char, (self.x, self.y))
        self.hitbox = (self.x, self.y, 64, 64)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        hitSound.play()
        font1 = pygame.font.SysFont('comicsans', 80)
        text = font1.render('You got Hit -10', 1, (255, 0, 0))
        win.blit(text, (320 - (text.get_width() // 2), 100))
        pygame.display.update()
        j = 0
        self.x = w_width // 2 - 32
        self.y = w_height - 64
        while j < 300:
            pygame.time.delay(10)
            j += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    j = 301
                    pygame.quit()

    def winner(self):
        winSound.play()
        font1 = pygame.font.SysFont('comicsans', 80)
        text = font1.render('You have won !!!', 1, (255, 0, 0))
        win.blit(text, (320 - (text.get_width() // 2), 100))
        pygame.display.update()
        self.x = w_width // 2 - 32
        self.y = w_height - 64
        j = 0
        while j < 300:
            pygame.time.delay(10)
            j += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    j = 301
                    pygame.quit()


# ***************************************** Moving obstacles **********************************************************

class ENEMY(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.end = end
        self.vel = 5
        self.hitbox = (self.x, self.y, 64, 64)

    def draw(self, win):
        self.move()
        win.blit(char_2, (self.x, self.y))
        self.hitbox = (self.x, self.y, 64, 64)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x >= w_width:
                self.x = -64
            else:
                self.x += self.vel


# ********************************************* fixed obstacles *******************************************************

class FIXED_OBSTACLE(object):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 64, 64)

    def draw(self, win):
        win.blit(char_3, (self.x, self.y))
        self.hitbox = (self.x, self.y, 64, 64)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


# ******************************************* redraw window ***********************************************************

def redrawGameWindow():
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 4 * 80 - 4 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 3 * 80 - 3 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 2 * 80 - 2 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 80 - 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64, w_width, 64))
    player[player_no].draw(win)
    player[2].draw(win)
    for i in ship:
        i.draw(win)
    for i in obstacle:
        i.draw(win)
    text_1 = font.render("Score: " + str(score[1]), 1, (0, 0, 0))
    text_2 = font.render("Score: " + str(score[2]), 1, (0, 0, 0))
    win.blit(text_1, (500, 20))
    win.blit(text_2, (10, 20))
    pygame.display.update()


# main Loop
# ********************************  creating objects of various classes  *********************************************
run = True

player = [0, PLAYER(w_width // 2 - 32, w_height - 64, 64, 64), PLAYER(w_width // 2 - 32, 0, 64, 64)]
ship = [ENEMY(-64, w_height - 64 - 80, 64, 64),
        ENEMY(-64 + 100, w_height - 2 * 64 - 2 * 80, 64, 64),
        ENEMY(-64 + 350, w_height - 3 * 64 - 3 * 80, 64, 64),
        ENEMY(-64 + 500, w_height - 4 * 64 - 4 * 80 + 3, 64, 64)]
font = pygame.font.SysFont('comicsans', 30, True, True)

obstacle = [FIXED_OBSTACLE(w_width // 3 - 32, w_height - 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 3 - 32, w_height - 64, 64, 64),
            FIXED_OBSTACLE(w_width // 4 - 32, w_height - 64 - 80 - 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 4 - 32, w_height - 64 - 80 - 64, 64, 64),
            FIXED_OBSTACLE(3 * w_width // 4 - 32, w_height - 64 - 80 - 64, 64, 64),
            FIXED_OBSTACLE(0, w_height - 64 - 2 * 80 - 2 * 64, 64, 64),
            FIXED_OBSTACLE(1 * w_width // 3 - 32, w_height - 64 - 2 * 80 - 2 * 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 3 - 32, w_height - 64 - 2 * 80 - 2 * 64, 64, 64),
            FIXED_OBSTACLE(w_width - 64, w_height - 64 - 2 * 80 - 2 * 64, 64, 64),
            FIXED_OBSTACLE(w_width // 4 - 32, w_height - 64 - 3 * 80 - 3 * 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 4 - 32, w_height - 64 - 3 * 80 - 3 * 64, 64, 64),
            FIXED_OBSTACLE(3 * w_width // 4 - 32, w_height - 64 - 3 * 80 - 3 * 64, 64, 64),
            FIXED_OBSTACLE(w_width // 3 - 32, w_height - 64 - 4 * 80 - 4 * 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 3 - 32, w_height - 64 - 4 * 80 - 4 * 64, 64, 64)]


def check(i):
    global score
    if player[player_no].hitbox[1] < i.hitbox[1] + i.hitbox[3] and player[player_no].hitbox[1] + player[player_no].hitbox[3] > i.hitbox[1]:
        if player[player_no].hitbox[0] + player[player_no].hitbox[2] > i.hitbox[0] and player[player_no].hitbox[0] < i.hitbox[0] + i.hitbox[2]:
            player[player_no].hit()
            score[1] -= 10


# **************************************************** main loop ******************************************************

while run:
    clock.tick(27)
    for i in ship:
        check(i)
    for i in obstacle:
        check(i)
    if player[player_no].y <= 2:
        player[player_no].winner()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in ship:
        i.move()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player[player_no].x > player[player_no].vel:
        player[player_no].x -= player[player_no].vel
    if keys[pygame.K_RIGHT] and player[player_no].x < w_width - player[player_no].width:
        player[player_no].x += player[player_no].vel
    if keys[pygame.K_UP] and player[player_no].y > player[player_no].vel:
        player[player_no].y -= player[player_no].vel
    if keys[pygame.K_DOWN] and player[player_no].y < w_height - player[player_no].height:
        player[player_no].y += player[player_no].vel
    redrawGameWindow()
pygame.quit()
