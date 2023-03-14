import pygame
from ui import Button
import game



display_dimensions = (1100, 800)
screen = pygame.display.set_mode(display_dimensions)

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (50, 50, 190)
red = (190, 50, 50)
grey = (100, 100, 100)

p1 = pygame.image.load("resources/tutorial/page1.png")
p2 = pygame.image.load("resources/tutorial/page2.png")
p3 = pygame.image.load("resources/tutorial/page3.png")
p4 = pygame.image.load("resources/tutorial/page4.png")
p5 = pygame.image.load("resources/tutorial/page5.png")
p6 = pygame.image.load("resources/tutorial/page6.png")
p7 = pygame.image.load("resources/tutorial/page7.png")
p8 = pygame.image.load("resources/tutorial/page8.png")
p9 = pygame.image.load("resources/tutorial/page9.png")
p10 = pygame.image.load("resources/tutorial/page10.png")
p11 = pygame.image.load("resources/tutorial/page11.png")
p12 = pygame.image.load("resources/tutorial/page12.png")

page = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]

next_text = "Next"

clock = pygame.time.Clock()
FPS = 10


def tutorial_screen():

    next_button = Button(display_dimensions, next_text, (300, 180), (200, 100), blue, text_color=white,
                               text_size=25, action="next")
    back_button = Button(display_dimensions, "Back", (-300, 180), (200, 100), blue, text_color=white,
                               text_size=25, action="back")

    buttons = [next_button,back_button]

    page_index = 0

    while True:
        screen.fill((2,48,32))
        screen.blit(page[page_index],(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "next":
                                if page_index < 11:
                                    page_index += 1
                                    screen.blit(page[page_index], (0, 0))
                                else:
                                    return
                            elif button.action == "back":
                                if page_index > 0:
                                    page_index -= 1
                                else:
                                    return
                            else:
                                print("Button action: {} does not exist".format(button.action))

            for button in buttons:
                button.display(game.game_display, pygame.mouse.get_pos())


            pygame.display.update()
            clock.tick(30)