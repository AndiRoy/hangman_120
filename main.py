import pygame
import button
import random

# Initialize pygame
pygame.init()

#display window dimensions
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Welcome to Hangman!')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 255, 255)
RED = (255,64,64)
GREEN = (244,244,244)
ANOTHA_RED = (238,106,80)
TUR = (102,205,170)

# Fonts
buttn_font = pygame.font.SysFont("hedvig letters serif", 20)
letGuess_font = pygame.font.SysFont("dubai", 40)
noti_font = pygame.font.SysFont("lucidafax", 20)
Resfont = pygame.font.SysFont('dubai', 35)

# Variables
word = ''
buttons = []
guessed = []
limbs = 0
guesses_left = 6
wrongPush = False #timing for the "wrong letter!" text to show up
wrongPush_time = 0


#images for hangman body
hangmanStatus = [pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman0.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman1.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman2.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman3.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman4.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman5.png").convert_alpha(),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman6.png").convert_alpha()]



# images for buttons/backgrounds/other assets
title_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/TITLE.png")
start_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/STARTBU.png")
exit_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/EXITBU.png")
backMenu_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/backgroundmenu.png").convert_alpha()


def redraw_game_window():
    global guessed
    global hangmanStatus
    global limbs
    global guesses_left

    guesses_label = noti_font.render(f"Guesses left: {guesses_left}", 1, BLACK)
    screen.blit(guesses_label, (50,400))

    #letter Buttons
    for i in range(len(buttons)):
        if buttons[i][4]: 
            pygame.draw.circle(screen, WHITE, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(screen, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            text = buttn_font.render(chr(buttons[i][5]), 1, BLACK)
            screen.blit(text, (buttons[i][1] - (text.get_width() / 2), buttons[i][2] - (text.get_height() / 2)))

    spaced = spaceCount(word, guessed)
    label1 = letGuess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    screen.blit(label1,(SCREEN_WIDTH/2 - length/2, 675))

    bodImg = hangmanStatus[limbs]
    screen.blit(bodImg, (SCREEN_WIDTH/2 - bodImg.get_width()/2 - 18, 80))

    if wrongPush and pygame.time.get_ticks() - wrongPush_time < 500:
        printguesses()
    

    pygame.display.update()

def spaceCount(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for i in range(len(word)):
        if word[i] != ' ':
            spacedWord += '_ '
            for j in range(len(guessedLetters)):
                if word[i].upper() == guessedLetters[j]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[i].upper() + ' '
        elif word[i] == ' ':
            spacedWord += ' '
    return spacedWord

#buttonds for menu  
start_button = button.Button(SCREEN_WIDTH / 4 - start_img.get_width() / 2 + 300, 350, start_img, .5)
exit_button = button.Button(3 * SCREEN_WIDTH / 4 - exit_img.get_width() / 2 + 300 , 350, exit_img, .5)


# Menu function
def menu():
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.blit(backMenu_img, (0, 0))
        if start_button.draw(screen):
            return "start"

        if exit_button.draw(screen):
            pygame.quit()
            quit()

        pygame.display.update()

# Main game function
def play_game():
    global word, buttons, guessed, limbs, guesses_left, wrongPush, wrongPush_time

    reset()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter is not None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(str(chr(letter))):
                        if limbs < 6:
                            limbs += 1
                            guesses_left -= 1
                            wrongPush = True
                            wrongPush_time = pygame.time.get_ticks()
                            printguesses()
                        else:
                            end()
                else:
                    print(spaceCount(word, guessed))
                    if spaceCount(word, guessed).count('_') == 0:
                        end(True)
            
        
        screen.fill((GREEN))
        redraw_game_window()
        pygame.time.delay(10)
        pygame.display.update()

        clock.tick(10)

#to be used in play(), tells user how many guesses they have left
def printguesses():
    wrongGu_label = noti_font.render(f"Incorrect Letter!", 1, RED)
    screen.blit(wrongGu_label, (700, 260))
    pygame.display.update()
    
    
    
def spaceCount(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

def validWord():
    file = open("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/words.txt")
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

def end(winner=False):
    global limbs
    
    

    if winner == True:
        label = Resfont.render("You Won!", 1, BLACK)
    else:
        label = Resfont.render("You Lost!", 1, RED)

    wordTxt = Resfont.render(word.upper(), 1, BLACK)
    wordWas = Resfont.render('The phrase was: ', 1, BLACK)

    screen.blit(wordTxt, (SCREEN_WIDTH/2 - wordTxt.get_width()/2 + 250, 350))
    screen.blit(wordWas, (SCREEN_WIDTH/2 - wordWas.get_width()/2 + 250, 300))
    screen.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2 + 250, 200))
    pygame.display.update()

    
    
    runAgain = noti_font.render("Press 'P' to play again or 'Q' to quit",1,BLACK  )
    screen.blit(runAgain, (SCREEN_WIDTH/2 - runAgain.get_width()/2 + 250, 450))
    pygame.display.update()

    
    userKey()
    
def userKey():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    reset()
                    pause = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
    reset()
    

def reset():
    global limbs
    global guessed
    global buttons
    global word
    global guesses_left
    
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = validWord()
    guesses_left = 6
    

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False
# Setup buttons
increase = round(SCREEN_WIDTH / 12)
button_radius = 30
for i in range(26):
    if i < 13:
        y = 40
        x = 35 + (increase * i)
    else:
        x = 35 + (increase * (i - 13))
        y = 105
    buttons.append([ANOTHA_RED, x, y, 30, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

# Main loop
while True:
    action = menu()

    if action == "start":
        play_game()


