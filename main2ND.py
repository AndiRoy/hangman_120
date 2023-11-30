import pygame
import button
import random

# Initialize pygame
pygame.init()

# Create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Welcome to Hangman!')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (240, 255, 255)

# Fonts
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)

# Variables
word = ''
buttons = []
guessed = []
hangmanStatus = [pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman0.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman1.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman2.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman3.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman4.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman5.png"),
                 pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/hangman6.png")]

limbs = 0

# Load button images
title_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/TITLE.png")
start_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/STARTBU.png")
exit_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/EXITBU.png")


def redraw_game_window():
    global guessed
    global hangmanStatus
    global limbs
    screen.fill(WHITE)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(screen, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(screen, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            screen.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    screen.blit(label1,(SCREEN_WIDTH/2 - length/2, 400))

    pic = hangmanStatus[limbs]
    screen.blit(pic, (SCREEN_WIDTH/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

def spacedOut(word, guessed=[]):
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
# Create button instances
start_button = button.Button(150, 250, start_img, .5)
exit_button = button.Button(500, 250, exit_img, .5)

# Menu function
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((202, 228, 241))
        screen.blit(title_img, (25, 100))

        if start_button.draw(screen):
            return "start"

        if exit_button.draw(screen):
            pygame.quit()
            quit()

        pygame.display.update()

# Main game function
def play_game():
    global word, buttons, guessed, limbs

    reset()

    while True:
        redraw_game_window()
        pygame.time.delay(10)
        screen.fill((202, 228, 241))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Your game logic goes here

        pygame.display.update()

# Helper functions (spacedOut, randomWord, buttonHit, end, reset, hang) go here
def spacedOut(word, guessed=[]):
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

def randomWord():
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
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    screen.fill(WHITE)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    screen.blit(wordTxt, (SCREEN_WIDTH/2 - wordTxt.get_width()/2, 295))
    screen.blit(wordWas, (SCREEN_WIDTH/2 - wordWas.get_width()/2, 245))
    screen.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False
# Main loop
while True:
    action = menu()

    if action == "start":
        play_game()
