import pygame
import button

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0, 32)
pygame.display.set_caption('Welcome to Hangman!')

#load button images

title_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/TITLE.png")

start_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/STARTBU.png")
exit_img = pygame.image.load("C:/Users/drea1/OneDrive/Documents/120Hangman/testing 120/EXITBU.png") 
#create button instances
start_button = button.Button(150, 250, start_img, .5)
exit_button = button.Button(500, 250, exit_img, .5)


#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	#title png "Welcome to hangman"LEFT OFF BERE
	screen.blit(title_img, (25, 100))  # Adjust the coordinates as needed

	if start_button.draw(screen):
		print('START')
	if exit_button.draw(screen):
			print('EXIT')
			pygame.quit()

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		

	pygame.display.update()

pygame.quit()
