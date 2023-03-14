import pygame
from deck import Deck
from ui import Text, Button, RadioGroup, Radio, Checkbox
import settings_manager, history_manager
import tutorial

vegas_rules = settings_manager.load_settings()['vegas_rules']

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (50, 50, 190)
red = (190, 50, 50)
grey = (100, 100, 100)

display_dimensions = (1100, 800)

pygame.init()

game_display = pygame.display.set_mode(display_dimensions)

# window Name
pygame.display.set_caption('Solitaire')

# window icon
icon = pygame.image.load('resources/solitaire_icon.png')
pygame.display.set_icon(icon)

# main game clock, ie this checks 10 times per second (FPS) for any update
clock = pygame.time.Clock()
FPS = 10

total_score = 0
if vegas_rules:
    total_score = -52


# quits the game
def quit_game():
    pygame.quit()
    quit()


# runs the 'win' screen... gives options to play again, go back to main menu, or quit the game
# also runs the game over screen for vegas rules... acts the same way and displays score
def win_screen():
    f = open("game_data/highscore.txt", "w")
    f.write(str(total_score))
    f.close()
    quit_button = Button(display_dimensions, "Quit", (250, 0), (200, 100), red, text_color=white, text_size=25, action="quit")
    play_again_button = Button(display_dimensions, "Play Again", (0, 0), (200, 100), blue, text_color=white, text_size=25, action="play_again")
    start_menu_button = Button(display_dimensions, "Start Menu", (-250, 0), (200, 100), green, text_color=white, text_size=25, action="start_menu")
    buttons = [quit_button, play_again_button, start_menu_button]
    if vegas_rules:
        win_text = Text(display_dimensions, (0, -200), "Game over. You scored "+str(total_score)+" points.", 60, black)
    else:
        win_text = Text(display_dimensions, (0, -200), "You Win!!!", 60, black)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        for button in buttons:
                            if button.check_if_clicked(mouse_pos):
                                if button.action == "quit":
                                    quit_game()
                                elif button.action == "play_again":
                                    game_loop()
                                elif button.action == "start_menu":
                                    start_menu()
                                else:
                                    print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        win_text.display(game_display)

        pygame.display.update()
        clock.tick(FPS)


def pause_screen():
    start_menu_button = Button(display_dimensions, "Start Menu", (-250, 0), (200, 100), green, text_color=white, text_size=25, action="start_menu")
    unpause_button = Button(display_dimensions, "Unpause", (0, 0), (200, 100), blue, text_color=white, text_size=25, action="unpause")
    quit_button = Button(display_dimensions, "Quit", (250, 0), (200, 100), red, text_color=white, text_size=25, action="quit")
    tutorial_button = Button(display_dimensions, "Tutorial", (0, 120), (200, 100), grey, text_color=white, text_size=25, action="tutorial")
    buttons = [start_menu_button, unpause_button, quit_button, tutorial_button]
    pause_text = Text(display_dimensions, (0, -200), "Paused", 60, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "start_menu":
                                start_menu()
                            elif button.action == "unpause":
                                return
                            elif button.action == "quit":
                                quit_game()
                            elif button.action == "tutorial":
                                tutorial.tutorial_screen()
                            else:
                                print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pause_text.display(game_display)

        pygame.display.update()
        clock.tick(FPS)


def game_loop():
    global total_score
    undo_button = Button(display_dimensions, "Undo", (10, 10), (30, 30), grey, centered=False, text_size=11, action="undo")
    restart_button = Button(display_dimensions, "Restart", (display_dimensions[0]-50, 10), (40, 30), grey, centered=False, text_size=10, action="restart")
    buttons = [undo_button, restart_button]

    deck = Deck()
    deck.load_cards()
    deck.shuffle_cards()
    deck.load_piles(display_dimensions)

    hm = history_manager.HistoryManager(deck)
    while True:
        if deck.check_for_win():
            win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    total_score = 0
                    game_loop()
                    # for testing if you can win. TODO change later
                elif event.key == pygame.K_w:
                    win_screen()
                elif event.key == pygame.K_ESCAPE:
                    pause_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    piles_to_update, valid_move, score = deck.handle_click(mouse_pos)
                    total_score += score
                    
                    deck.update(piles_to_update, display_dimensions[1])
                    if valid_move:
                        hm.valid_move_made(deck)

                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "undo":
                                deck = hm.undo(deck)
                                total_score -= (5 if total_score != 0 else 0)
                            if button.action == "restart":
                                game_loop()
                if event.button == 3:
                    deck.handle_right_click(mouse_pos)

        game_display.fill([2, 48, 32])  # background color #023020
        
        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())
        
        score_text = Text(display_dimensions, (0, -380), "Score: {}".format(total_score), 20, white)
        score_text.display(game_display)
        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


def options_menu():
    settings = settings_manager.load_settings()

    title_text = Text(display_dimensions, (0, -370), "Options", 40, black)
    about_text = Text(display_dimensions, (0, 350), "2023", 14, black)

    back_button = Button(display_dimensions, "Back", (10, 25), (75, 25), red, centered=False, text_color=white, text_size=14, action="back")
    buttons = [back_button]

    #draw_three_checkbox = Checkbox(display_dimensions, (10, 100), centered=False, checked=settings['draw_three'])
    #draw_three_label = Text(display_dimensions, (40, 100), "Draw three cards from deck", 14, black, centered=False)

    vegas_rules_checkbox = Checkbox(display_dimensions, (10, 100), centered=False, checked=settings['vegas_rules'])
    vegas_rules_label = Text(display_dimensions, (40, 100), "Play with Vegas Rules", 14, black, centered=False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "back":
                                #settings_manager.save_settings({'draw_three': draw_three_checkbox.checked})
                                settings_manager.save_settings({'vegas_rules': vegas_rules_checkbox.checked})
                                global vegas_rules
                                vegas_rules = settings_manager.load_settings()['vegas_rules']
                                global total_score
                                if vegas_rules:
                                    total_score = -52
                                else:
                                    total_score = 0
                                start_menu()
                            else:
                                print("Button action: {} does not exist".format(button.action))

                    # draw_three_checkbox.check_if_clicked(mouse_pos)
                    vegas_rules_checkbox.check_if_clicked(mouse_pos)

        game_display.fill(white)

        title_text.display(game_display)
        about_text.display(game_display)

        # draw_three_label.display(game_display)
        # draw_three_checkbox.display(game_display)

        vegas_rules_checkbox.display(game_display)
        vegas_rules_label.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(FPS)


def start_menu():
    title = Text(display_dimensions, (0, -100), "Solitaire", 50, black)

    play_button = Button(display_dimensions, "Play", (0, 0), (100, 50), blue, text_color=white, text_size=26, action="start_game")
    quit_button = Button(display_dimensions, "Quit", (200, 0), (100, 50), red, text_color=white, action="quit")
    options_button = Button(display_dimensions, "Options", (-200, 0), (100, 50), grey, text_color=white, action="options")
    buttons = [play_button, quit_button, options_button]

    global vegas_rules
    vegas_rules = settings_manager.load_settings()['vegas_rules']
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "start_game":
                                game_loop()
                            elif button.action == "quit":
                                quit_game()
                            elif button.action == "options":
                                options_menu()
                                pass
                            else:
                                print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        title.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(FPS)


