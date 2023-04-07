import pygame
import random
import os
import time
import math

pygame.init()

display_info = pygame.display.Info()
WIDTH, HEIGHT = (display_info.current_w / 1.3), (display_info.current_h / 1.3)
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('WW1 Telegrapher Game (Mr. Walls is Cool)')

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TITLE_BG = pygame.image.load(os.path.join('assets', 'ww1bg2.jpg'))
INTRO_BG = pygame.image.load(os.path.join('assets', 'ww1bg3.jpg'))
SOLDIER = pygame.image.load(os.path.join('assets', 'soldier.png'))
SOLDIER_BG = pygame.image.load(os.path.join('assets', 'ww1bg.jpg'))
TRANS_BG = pygame.image.load(os.path.join('assets', 'telegraphlines.jpg'))
MORSE_KEY = pygame.image.load(os.path.join('assets', 'morsekey.jpg'))

SOLDIER_IMG = pygame.transform.scale(SOLDIER, (WIDTH / 20, HEIGHT / 15)) and pygame.transform.flip(SOLDIER, True, False)
PLAY_BUTTON = pygame.Rect(WIDTH / 2 - 100, HEIGHT - 200, 200, 70)
SKIP_INTRO_BUTTON = pygame.Rect(WIDTH - 100, HEIGHT - 40, 100, 40)
NEXT_INTRO_BUTTON = pygame.Rect(WIDTH / 2 - 50, HEIGHT - 40, 100, 40)
DASH_BUTTON = pygame.Rect(WIDTH / 2, HEIGHT / 9, 60, 60)
DOT_BUTTON = pygame.Rect(WIDTH / 2 + 70, HEIGHT / 9, 60, 60)
SLASH_BUTTON = pygame.Rect(WIDTH / 2 + 140, HEIGHT / 9, 60, 60)
SPACE_BUTTON = pygame.Rect(WIDTH / 2, HEIGHT / 9 + 70, 140, 60)

title_font = pygame.font.SysFont('arial', 70)
play_button_font = pygame.font.SysFont('sansserif', 60)
intro_skip_font = pygame.font.SysFont('sansserif', 40)
intro_font = pygame.font.SysFont('sansserif', 25)
intro_tite_font = pygame.font.SysFont('sansserif', 40)
next_button_font = pygame.font.SysFont('sansserif', 40)
guy_font = pygame.font.SysFont('gadugi', 35)
trans_font = pygame.font.SysFont('arial', 20)
trans_button_font = pygame.font.SysFont('arial', 40)

run = True
clock = pygame.time.Clock()
stage = 'title'
intro_title = 'The Invention of the Telegraph'
intro_text1 = ['The telegraph was invented in the early 19th century and revolutionized communication by allowing',
               'messages to be sent quickly over long distances. In 1837, Samuel Morse developed the Morse code,',
               'a system of dots and dashes that could be used to transmit messages over a wire. ',
               'In 1844, he sent the first telegraph message from Washington D.C. to Baltimore, which read: ',
               '"What hath God wrought?" The telegraph quickly spread throughout the world, and by the end ',
               'of the 19th century, it had become the dominant means of long-distance communication.']
intro_text2 = ['During World War I, the telegraph played a critical role in military communication.',
               'Messages were sent using telegraph wires laid along the front lines, which allowed',
               'commanders to quickly communicate orders and intelligence. The use of telegraphs also',
               'facilitated communication between military headquarters and supply depots,',
               'enabling the efficient movement of troops and supplies. However, the telegraph',
               'was vulnerable to interception and sabotage, and both sides employed codebreakers',
               'to intercept and decipher enemy messages. Despite its limitations, the telegraph',
               'remained a vital tool of wartime communication and helped shape the course of the war.']
intro_text3 = ['First, you will receive a phrase to translate. You must translate this within 60 seconds',
               'or we will lose the war. Read each letter from the phrase and click the dots and',
               'dashes to translate the letters and send them on their way. Separate each letter',
               'with a space and each word with a slash (space before and after slash).',
               'Example:',
               'hi man',
               'Translates to:',
               '.... .. / -- .- -.']

trans_prog = 0
trans = ['send backup', 'two troops captured', 'join germany', 'fallen soldier', 'war over']
current_trans = random.choice(trans)
trans_input = ''
timer, tic = False, 0
ref_clock = 60


def check_trans(start, end, prog, transs):
    length = float(f'{end - start:0.2f}')
    if length < 60:
        prog += 1

        if prog >= 3:
            return 'win', None, None

        next_trans = random.choice(transs)
        return 'guy', prog, next_trans

    else:
        return 'loose', None, None


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            PLAY_BUTTON = pygame.Rect(WIDTH / 2 - 100, HEIGHT - 200, 200, 70)
            SKIP_INTRO_BUTTON = pygame.Rect(WIDTH - 100, HEIGHT - 40, 100, 40)
            NEXT_INTRO_BUTTON = pygame.Rect(WIDTH / 2 - 50, HEIGHT - 40, 100, 40)
            DASH_BUTTON = pygame.Rect(WIDTH / 2, HEIGHT / 9, 60, 60)
            DOT_BUTTON = pygame.Rect(WIDTH / 2 + 70, HEIGHT / 9, 60, 60)
            SLASH_BUTTON = pygame.Rect(WIDTH / 2 + 140, HEIGHT / 9, 60, 60)
            SPACE_BUTTON = pygame.Rect(WIDTH / 2, HEIGHT / 9 + 70, 140, 60)

        if stage == 'title':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.collidepoint(event.pos):
                    stage = 'intro'

        elif stage == 'intro':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SKIP_INTRO_BUTTON.collidepoint(event.pos):
                    stage = 'guy'
                elif NEXT_INTRO_BUTTON.collidepoint(event.pos):
                    if intro_title == 'The Invention of the Telegraph':
                        intro_title = 'The Telegraph in WW1'
                    elif intro_title == 'The Telegraph in WW1':
                        intro_title = 'Instructions'
                    else:
                        stage = 'guy'


        elif stage == 'trans':
            if current_trans == 'send backup' and \
                    trans_input == '... . -. -.. / -... .- -.-. -.- ..- .--.':
                trans.remove(current_trans)
                stage, trans_prog, current_trans = check_trans(tic, time.perf_counter(), trans_prog, trans)
                trans_input, ref_clock, timer = '', 60, False
            elif current_trans == 'two troops captured' and \
                    trans_input == '- .-- --- / - .-. --- --- .--. ... / -.-. .- .--. - ..- .-. . -..':
                trans.remove(current_trans)
                stage, trans_prog, current_trans = check_trans(tic, time.perf_counter(), trans_prog, trans)
                trans_input, ref_clock, timer = '', 60, False
            elif current_trans == 'join germany' and \
                    trans_input == '.--- --- .. -. / --. . .-. -- .- -. -.--':
                trans.remove(current_trans)
                stage, trans_prog, current_trans = check_trans(tic, time.perf_counter(), trans_prog, trans)
                trans_input, ref_clock, timer = '', 60, False
            elif current_trans == 'fallen soldier' and \
                    trans_input == '..-. .- .-.. .-.. . -. / ... --- .-.. -.. .. . .-.':
                trans.remove(current_trans)
                stage, trans_prog, current_trans = check_trans(tic, time.perf_counter(), trans_prog, trans)
                trans_input, ref_clock, timer = '', 60, False
            elif current_trans == 'war over' and \
                    trans_input == '.-- .- .-. / --- ...- . .-.':
                trans.remove(current_trans)
                stage, trans_prog, current_trans = check_trans(tic, time.perf_counter(), trans_prog, trans)
                trans_input, ref_clock, timer = '', 60, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if DOT_BUTTON.collidepoint(event.pos):
                    trans_input += '.'
                    if not timer:
                        tic = time.perf_counter()
                        timer = True
                elif DASH_BUTTON.collidepoint(event.pos):
                    trans_input += '-'
                    if not timer:
                        tic = time.perf_counter()
                        timer = True
                elif SLASH_BUTTON.collidepoint(event.pos):
                    trans_input += '/'
                    if not timer:
                        tic = time.perf_counter()
                        timer = True
                elif SPACE_BUTTON.collidepoint(event.pos):
                    trans_input += ' '
                    if not timer:
                        tic = time.perf_counter()
                        timer = True

    if stage == 'title':
        WIN.blit(pygame.transform.scale(TITLE_BG, (WIDTH, HEIGHT)), (0, 0))

        pygame.draw.rect(WIN, WHITE, PLAY_BUTTON)
        WIN.blit(play_button_font.render('PLAY', True, BLACK),
                 (PLAY_BUTTON.x + 47, PLAY_BUTTON.y + 17))

        x = pygame.time.get_ticks() / 3 % 1000
        y = math.sin(x / 70) * 30 + 100
        TITLE_TEXT = title_font.render('WW1 Telegrapher', True, BLACK, WHITE)
        WIN.blit(TITLE_TEXT, (PLAY_BUTTON.x - 130, y))

    elif stage == 'intro':
        WIN.blit(pygame.transform.scale(INTRO_BG, (WIDTH, HEIGHT)), (0, 0))

        pygame.draw.rect(WIN, BLACK, SKIP_INTRO_BUTTON)
        WIN.blit(intro_skip_font.render('SKIP', True, WHITE),
                 (SKIP_INTRO_BUTTON.x + 10, SKIP_INTRO_BUTTON.y + 10))

        WIN.blit(intro_tite_font.render(intro_title, True, BLACK), (WIDTH / 13, HEIGHT / 13))

        text_height = HEIGHT / 6
        if intro_title == 'The Invention of the Telegraph':
            for text in intro_text1:
                WIN.blit(intro_font.render(text, True, BLACK, WHITE), (WIDTH / 13, text_height))
                text_height += 20
        elif intro_title == 'The Telegraph in WW1':
            for text in intro_text2:
                WIN.blit(intro_font.render(text, True, BLACK, WHITE), (WIDTH / 13, text_height))
                text_height += 20
        elif intro_title == 'Instructions':
            for text in intro_text3:
                WIN.blit(intro_font.render(text, True, BLACK, WHITE), (WIDTH / 13, text_height))
                text_height += 20

        pygame.draw.rect(WIN, BLACK, NEXT_INTRO_BUTTON)
        WIN.blit(next_button_font.render('NEXT', True, WHITE),
                 (NEXT_INTRO_BUTTON.x + 10, NEXT_INTRO_BUTTON.y + 10))

    elif stage == 'guy':
        WIN.blit(pygame.transform.scale(SOLDIER_BG, (WIDTH, HEIGHT)), (0, 0))
        WIN.blit(pygame.transform.scale(SOLDIER_IMG, (WIDTH / 3.5, HEIGHT)), (20, HEIGHT / 5))
        WIN.blit(guy_font.render('We need you to translate this sentence!', True, BLACK, WHITE),
                 (WIDTH / 5, HEIGHT / 5))
        WIN.blit(trans_font.render(current_trans, True, BLACK, WHITE), (WIDTH / 2, HEIGHT / 2))
        pygame.display.update()
        pygame.time.delay(5000)
        stage = 'trans'

    elif stage == 'trans':
        WIN.blit(pygame.transform.scale(TRANS_BG, (WIDTH, HEIGHT)), (0, 0))
        WIN.blit(trans_font.render('Translate: ' + current_trans, True, WHITE, BLACK), (WIDTH / 10, HEIGHT / 8))

        pygame.draw.rect(WIN, BLACK, DASH_BUTTON)
        WIN.blit(trans_button_font.render('-', True, WHITE),
                 (DASH_BUTTON.x + (DASH_BUTTON.w / 2) - 6, DASH_BUTTON.y + 5))

        pygame.draw.rect(WIN, BLACK, DOT_BUTTON)
        WIN.blit(trans_button_font.render('.', True, WHITE),
                 (DOT_BUTTON.x + (DOT_BUTTON.w / 2) - 6, DOT_BUTTON.y + 5))

        pygame.draw.rect(WIN, BLACK, SLASH_BUTTON)
        WIN.blit(trans_button_font.render('/', True, WHITE),
                 (SLASH_BUTTON.x + (SLASH_BUTTON.w / 2) - 6, SLASH_BUTTON.y + 5))

        pygame.draw.rect(WIN, BLACK, SPACE_BUTTON)
        WIN.blit(trans_button_font.render('(space)', True, WHITE),
                 (SPACE_BUTTON.x + 15, SPACE_BUTTON.y + 5))

        WIN.blit(pygame.transform.scale(MORSE_KEY, (WIDTH / 2, HEIGHT / 3)),
                 (WIDTH / 2 - ((WIDTH / 2) / 2), HEIGHT / 2 + 30))
        WIN.blit(trans_font.render(trans_input, True, BLACK),
                 (WIDTH / 2, HEIGHT / 2 - 40))

        if timer:
            WIN.blit(trans_font.render(f'{ref_clock:0.2f}', True, WHITE, BLACK), (0, 0))
            ref_clock -= 0.016
        if ref_clock < 0:
            stage = 'loose'

    elif stage == 'win':
        WIN.fill(WHITE)
        WIN.blit(title_font.render('WE WIN THE WAR!', True, BLACK), (WIDTH / 4, HEIGHT / 3))

    elif stage == 'loose':
        WIN.fill(WHITE)
        WIN.blit(title_font.render('WE LOOSE THE WAR :(', True, BLACK), (WIDTH / 5, HEIGHT / 3))

    pygame.display.update()
