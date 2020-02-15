# lets start pyGAMING
import pygame
import configparser
pygame.init()
configParser = configparser.RawConfigParser()
configParser.read('config.cfg')
name = configParser.get('info', 'Name')
win = pygame.display.set_mode((640, 866 - 80))
pygame.display.set_caption(name)
# ********************************************* config messages *******************************************************
gameover = configParser.get('info', 'gameover')
success = configParser.get('info', 'success')
pone_win = configParser.get('info', 'Pwin')
pone_los = configParser.get('info', 'Plos')

# ********************************************* GLOBAL VARIABLES ******************************************************
w_width = configParser.getint('info', 'W_WIDTH')
w_height = configParser.getint('info', 'W_HEIGHT')
dead = [False, False]
success = [False, False]
score = [0, 0]  # here score[1] represents player 1, score[2] represents player 2
player_no = 0  # reports player no. ----- player_1 = 0, player_2 = 1
# ************************************************* Creating Flags ****************************************************
flag = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# *********************************************** Sounds **************************************************************

winSound = pygame.mixer.Sound('winn.wav')
# hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('main_music.mp3')
pygame.mixer.music.play(-1)

# *********************************************** Images **************************************************************

bg = pygame.image.load('water.jpg')
char = pygame.image.load('spaceship.png')
char_2 = pygame.image.load('ship.png')
char_3 = pygame.image.load('tower.png')
char_4 = pygame.image.load('ispaceship.png')

# ************************************************ Clock Time *********************************************************
clock = pygame.time.Clock()


# ***************************************** Players *******************************************************************
class PLAYER(object):
    def __init__(self, x, y, width, height, play_no, level):
        self.level = level
        self.time_start = 0
        self.play_no = play_no
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hit_box = (self.x, self.y, 64, 64)
        self.time = 0

    def draw(self, win):
        if self.play_no == 0:
            win.blit(char, (self.x, self.y))
        else:
            win.blit(char_4, (self.x, self.y))
        self.hit_box = (self.x, self.y, 64, 64)
        pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        # pygame.mixer.hitSound.play(1)
        win.fill([0, 0, 0])
        pygame.display.update()
        music = pygame.mixer.music.load('hit2.mp3')
        pygame.mixer.music.play(1)
        print("Hit !!! player no : " + str(self.play_no) + " y : " + str(self.y) + " x : ", self.x)
        font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 80)
        text = font1.render('G A M E O V E R', 1, (255, 255, 255))
        win.blit(text, (320 - (text.get_width() // 2), 400))
        pygame.display.update()
        j = 0
        time_end = pygame.time.get_ticks()
        self.time = time_end - self.time_start
        self.x = w_width // 2 - 32
        if self.play_no == 0:
            self.y = w_height - 64
        elif self.play_no == 1:
            self.y = 0
        while j < 350:
            pygame.time.delay(10)
            j += 1
            for x_event in pygame.event.get():
                if x_event.type == pygame.QUIT:
                    j = 351
                    pygame.quit()
        music = pygame.mixer.music.load('main_music.mp3')
        pygame.mixer.music.play(-1)

    def winner(self):
        win.fill([0, 0, 0])
        pygame.display.update()
        music = pygame.mixer.music.load('Ending.mp3')
        pygame.mixer.music.play(1)
        configParser.get('info', 'Name')
        font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 50)
        text = font1.render('Success !!!', 1, (255, 255, 255))
        win.blit(text, (320 - (text.get_width() // 2), 200))
        pygame.display.update()
        time_end = pygame.time.get_ticks()
        self.time = time_end - self.time_start
        self.x = w_width // 2 - 32
        if player_no == 0:
            self.y = w_height - 64
        else:
            self.y = 0
        # self.y = w_height - 64
        j = 0
        while j < 300:
            pygame.time.delay(10)
            j += 1
            for x_event in pygame.event.get():
                if x_event.type == pygame.QUIT:
                    j = 301
                    pygame.quit()
        music = pygame.mixer.music.load('main_music.mp3')
        pygame.mixer.music.play(-1)


# ***************************************** Moving obstacles **********************************************************

class ENEMY(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y + 7
        self.width = width
        self.height = height
        # self.end = end
        self.vel = 3
        self.hit_box = (self.x, self.y, 64, 64)
        self.z = 0

    def move(self, v):
        if self.vel > 0:
            if self.x >= w_width:
                self.x = -64
            else:
                self.z = v
                self.x += self.vel + self.z * 0.5
                print(self.vel + self.z * 0.5)

    def draw(self, win):
        self.move(self.z)
        win.blit(char_2, (self.x, self.y))
        self.hit_box = (self.x, self.y + 3, 64, 64 - 8 - 3)
        pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)


# ********************************************* fixed obstacles *******************************************************

class FIXED_OBSTACLE(object):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hit_box = (self.x, self.y, 64, 64)

    def draw(self, win):
        win.blit(char_3, (self.x, self.y))
        self.hit_box = (self.x, self.y, 64, 64)
        pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)


# ******************************************* redraw window ***********************************************************

def redraw_game_window():
    # win.blit(bg, (0, 0))
    win.fill([0, 150, 255])
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 5 * 80 - 5 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 4 * 80 - 4 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 3 * 80 - 3 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 2 * 80 - 2 * 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64 - 80 - 64, w_width, 64))
    pygame.draw.rect(win, (150, 75, 0), (0, w_height - 64, w_width, 64))
    player[player_no].draw(win)
    # player[2].draw(win)
    for x in ship:
        x.draw(win)
    for x in obstacle:
        x.draw(win)
    text_1 = font.render("Score P1: " + str(score[0]), 1, (0, 0, 0))
    text_2 = font.render("Score P2: " + str(score[1]), 1, (0, 0, 0))
    win.blit(text_1, (475, 20))
    win.blit(text_2, (10, 20))
    text_3 = font.render("Level P1: " + str(player[0].level), 1, (0, 0, 0))
    text_4 = font.render("Level P2: " + str(player[1].level), 1, (0, 0, 0))
    win.blit(text_3, (475, w_height - 44))
    win.blit(text_4, (10, w_height - 44))
    pygame.display.update()


# main Loop
# ********************************  creating objects of various classes  *********************************************
run = True

player = [PLAYER(w_width // 2 - 32, w_height - 64, 64, 64, 0, 0), PLAYER(w_width // 2 - 32, 0, 64, 64, 1, 0)]
ship = [ENEMY(-64, w_height - 64 - 80, 64, 64),
        ENEMY(-64 + 100, w_height - 2 * 64 - 2 * 80, 64, 64),
        ENEMY(-64 + 350, w_height - 3 * 64 - 3 * 80, 64, 64),
        ENEMY(-64 + 500, w_height - 4 * 64 - 4 * 80 + 3, 64, 64),
        ENEMY(-64 + 350, w_height - 5 * 64 - 5 * 80 + 3, 64, 64)]
font = pygame.font.SysFont(configParser.get('info', 'FONT'), 30, True, True)

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
            FIXED_OBSTACLE(0, w_height - 64 - 4 * 80 - 4 * 64, 64, 64),
            FIXED_OBSTACLE(1 * w_width // 3 - 32, w_height - 64 - 4 * 80 - 4 * 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 3 - 32, w_height - 64 - 4 * 80 - 4 * 64, 64, 64),
            FIXED_OBSTACLE(w_width - 64, w_height - 64 - 4 * 80 - 4 * 64, 64, 64),
            FIXED_OBSTACLE(w_width // 3 - 32, w_height - 64 - 5 * 80 - 5 * 64, 64, 64),
            FIXED_OBSTACLE(2 * w_width // 3 - 32, w_height - 64 - 5 * 80 - 5 * 64, 64, 64)]


# ************************************************** collision check **************************************************
def check(i):
    global score, player_no, flag
    if player[player_no].hit_box[1] < i.hit_box[1] + i.hit_box[3]:
        if player[player_no].hit_box[1] + player[player_no].hit_box[3] > i.hit_box[1]:
            if player[player_no].hit_box[0] + player[player_no].hit_box[2] > i.hit_box[0]:
                if player[player_no].hit_box[0] < i.hit_box[0] + i.hit_box[2]:
                    player[player_no].hit()
                    dead[player_no] = True
                    score[player_no] -= 10
                    flag[0] = 0
                    flag[1] = 0
                    flag[2] = 0
                    flag[3] = 0
                    flag[4] = 0
                    flag[5] = 0
                    flag[6] = 0
                    flag[7] = 0
                    flag[8] = 0
                    flag[9] = 0
                    if player_no == 0:
                        player_no = 1
                    else:
                        player_no = 0
                    player[player_no].time_start = pygame.time.get_ticks()
                    redraw_game_window()


# **************************************************** main loop ******************************************************
player[0].time_start = pygame.time.get_ticks()
while run:
    # print(player[0].time_start)
    clock.tick(27)
# ************************************************ hit/not hit ********************************************************
    for i in ship:
        check(i)
    for i in obstacle:
        check(i)
# ************************************************ check win/lose *****************************************************
    if player[player_no].y <= 2 and player_no == 0:
        score[0] += 15
        player[player_no].winner()
        success[player_no] = True
        player_no = 1
        flag[0] = 0
        flag[1] = 0
        flag[2] = 0
        flag[3] = 0
        flag[4] = 0
        flag[5] = 0
        flag[6] = 0
        flag[7] = 0
        flag[8] = 0
        flag[9] = 0
        player[player_no].time_start = pygame.time.get_ticks()
        redraw_game_window()
    elif player[player_no].y >= (w_height - 2 - 64) and player_no == 1:
        score[1] += 15
        player[player_no].winner()
        success[player_no] = True
        player_no = 0
        flag[0] = 0
        flag[1] = 0
        flag[2] = 0
        flag[3] = 0
        flag[4] = 0
        flag[5] = 0
        flag[6] = 0
        flag[7] = 0
        flag[8] = 0
        flag[9] = 0
        player[player_no].time_start = pygame.time.get_ticks()
        redraw_game_window()
# ************************************************ End of the Game ****************************************************
    if dead[1] or success[1]:
        win.fill([0, 0, 0])
        pygame.display.update()
        music = pygame.mixer.music.load('Ending.mp3')
        pygame.mixer.music.play(1)
        font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 30)
        text_1 = font1.render('Player 1 : Score: ' + str(score[0]), 1, (255, 0, 0))
        text_2 = font1.render('Player 2 : Score: ' + str(score[1]), 1, (255, 0, 0))
        text_3 = font1.render('Player 1 : Time: ' + str(player[0].time / 1000), 1, (255, 0, 0))
        text_4 = font1.render('Player 1 : Time: ' + str(player[1].time / 1000), 1, (255, 0, 0))
        win.blit(text_1, (50, 400))
        win.blit(text_3, (640 - 40 - (text_2.get_width()), 400))
        win.blit(text_2, (50, 500))
        win.blit(text_4, (640 - 40 - (text_2.get_width()), 500))
        if score[0] > score[1]:
            font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 50)
            text_1 = font1.render('Player 1 : Won !!! ', 1, (255, 0, 0))
            text_2 = font1.render('Player 2 : Lost !!! ', 1, (255, 0, 0))
            win.blit(text_1, (320 - (text_1.get_width() // 2), 200))
            win.blit(text_2, (320 - (text_2.get_width() // 2), 300))
            pygame.display.update()
        elif score[1] > score[0]:
            font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 50)
            text_1 = font1.render('Player 1 : Lost !!! ', 1, (255, 0, 0))
            text_2 = font1.render('Player 2 : Won !!! ', 1, (255, 0, 0))
            win.blit(text_1, (320 - (text_1.get_width() // 2), 200))
            win.blit(text_2, (320 - (text_2.get_width() // 2), 300))
            pygame.display.update()
        else:
            font1 = pygame.font.SysFont(configParser.get('info', 'FONT'), 50)
            # text_0 = font1.render('Time 1 : ' + str(player[0].time), 1, (255, 0, 0))
            # text_1 = font1.render('Time 2 : ' + str(player[1].time), 1, (255, 0, 0))
            if str(player[0].time) < str(player[1].time):
                text_2 = font1.render('Player 1 : Won !!! ', 1, (255, 0, 0))
                text_3 = font1.render('Player 2 : Lost !!! ', 1, (255, 0, 0))
            elif str(player[0].time) > str(player[1].time):
                text_2 = font1.render('Player 2 : Won !!! ', 1, (255, 0, 0))
                text_3 = font1.render('Player 1 : Lost !!! ', 1, (255, 0, 0))
            else:
                text_2 = font1.render('Player 2 : Draw !!! ', 1, (255, 0, 0))
                text_3 = font1.render('Player 1 : Draw !!! ', 1, (255, 0, 0))
            # win.blit(text_0, (320 - (text_1.get_width() // 2), 100))
            # win.blit(text_1, (320 - (text_1.get_width() // 2), 200))
            win.blit(text_2, (320 - (text_2.get_width() // 2), 200))
            win.blit(text_3, (320 - (text_2.get_width() // 2), 300))
            pygame.display.update()
        if success[0]:
            player[0].level += 1
        if success[1]:
            player[1].level += 1
        j = 0
        while j < 650:
            pygame.time.delay(10)
            j += 1
            for x_event in pygame.event.get():
                if x_event.type == pygame.QUIT:
                    j = 651
                    pygame.quit()
        score[1] = 0
        score[0] = 0
        dead[0] = False
        dead[1] = False
        success[0] = False
        success[1] = False
        player[0].time_start = pygame.time.get_ticks()
        music = pygame.mixer.music.load('main_music.mp3')
        pygame.mixer.music.play(-1)

# *************************************************** Scoring *********************************************************
    if player_no == 0:
        if player[player_no].y < w_width - 2 * 64 - 2 and flag[0] == 0:
            score[0] += 5
            print("scored 0")
            flag[0] = 1
        if player[player_no].y < w_width - 2 * 64 - 80 - 2 and flag[1] == 0:
            score[0] += 10
            print("scored 0")
            flag[1] = 1
        if player[player_no].y < w_width - 3 * 64 - 80 - 2 and flag[2] == 0:
            score[0] += 5
            print("scored 0")
            flag[2] = 1
        if player[player_no].y < w_width - 3 * 64 - 2 * 80 - 2 and flag[3] == 0:
            score[0] += 10
            print("scored 0")
            flag[3] = 1
        if player[player_no].y < w_width - 4 * 64 - 2 * 80 - 2 and flag[4] == 0:
            score[0] += 5
            print("scored 0")
            flag[4] = 1
        if player[player_no].y < w_width - 4 * 64 - 3 * 80 - 2 and flag[5] == 0:
            score[0] += 10
            print("scored 0")
            flag[5] = 1
        if player[player_no].y < w_width - 5 * 64 - 3 * 80 - 2 and flag[6] == 0:
            score[0] += 5
            print("scored 0")
            flag[6] = 1
        if player[player_no].y < w_width - 5 * 64 - 3 * 80 - 2 and flag[7] == 0:
            score[0] += 10
            print("scored 0")
            flag[7] = 1
        if player[player_no].y < w_width - 5 * 64 - 3 * 80 - 2 and flag[8] == 0:
            score[0] += 5
            print("scored 0")
            flag[8] = 1
        if player[player_no].y < 4 and flag[9] == 0:
            score[0] += 10
            print("scored 0")
            flag[9] = 1
    if player_no == 1:
        if player[player_no].y > 5 * 64 + 5 * 80 + 2 and flag[0] == 0:
            score[1] += 10
            print("scored 0")
            flag[0] = 1
        if player[player_no].y > 5 * 64 + 4 * 80 + 2 and flag[1] == 0:
            score[1] += 5
            print("scored 0")
            flag[1] = 1
        if player[player_no].y > 4 * 64 + 4 * 80 + 2 and flag[2] == 0:
            score[1] += 10
            print("scored 0")
            flag[2] = 1
        if player[player_no].y > 4 * 64 + 3 * 80 + 2 and flag[3] == 0:
            score[1] += 5
            print("scored 0")
            flag[3] = 1
        if player[player_no].y > 3 * 64 + 3 * 80 + 2 and flag[4] == 0:
            score[1] += 10
            print("scored 0")
            flag[4] = 1
        if player[player_no].y > 3 * 64 + 2 * 80 + 2 and flag[5] == 0:
            score[1] += 5
            print("scored 0")
            flag[5] = 1
        if player[player_no].y > 2 * 64 + 2 * 80 + 2 and flag[6] == 0:
            score[1] += 10
            print("scored 0")
            flag[6] = 1
        if player[player_no].y > 2 * 64 + 80 + 2 and flag[7] == 0:
            score[1] += 5
            print("scored 0")
            flag[7] = 1
        if player[player_no].y > 64 + 80 + 2 and flag[8] == 0:
            score[1] += 10
            print("scored 0")
            flag[8] = 1
        if player[player_no].y > 64 + 2 and flag[9] == 0:
            score[1] += 5
            print("scored 0")
            flag[9] = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in ship:
        i.move(player[player_no].level)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player[player_no].x > player[player_no].vel:
        player[player_no].x -= player[player_no].vel
    if keys[pygame.K_RIGHT] and player[player_no].x < w_width - player[player_no].width:
        player[player_no].x += player[player_no].vel
    if keys[pygame.K_UP] and player[player_no].y > player[player_no].vel:
        player[player_no].y -= player[player_no].vel
    if keys[pygame.K_DOWN] and player[player_no].y < w_height - player[player_no].height:
        player[player_no].y += player[player_no].vel
    redraw_game_window()
pygame.quit()
