from threading import Thread
import pygame
from pyttsx3 import init
from time import time, sleep

text_file= "text.txt"   # file location
speaking_speed = 100    # wpm

# text extraction
text = open(text_file, 'r').read()
sentece_list = text.split('\n')


# narration function
def narrate():
    
    final_text = ""
    for i in sentece_list:
        final_text += i + " "

    engine = init()
    engine.setProperty('rate', speaking_speed)
    engine.say(final_text)
    engine.runAndWait()


# diplying funtion
def display():

    pygame.init()
    pygame.font.init()

    w, h = 720, 320         # window dimensions
    fps = 60                #frames per second

    font = pygame.font.SysFont('Comic Sans MS', 30)

    win = pygame.display.set_mode((w, h))
    pygame.display.set_caption("readify screen")
    back_clr = (230, 230, 200)
    high_clr = (200, 150, 50)
    txt_clr = (0, 0, 45)

    current_time = time()
    high_word, high_sentence = 0, 0
    s = 0

    def draw(window, high_word, high_sentence):
        window.fill(back_clr)
        
        pos = [15, 50]
        clr = back_clr

        for s, sentence in enumerate(sentece_list): 
            words = sentence.split(' ')
            for w, word in enumerate(words):

                if high_word == w and high_sentence == s:
                    clr = high_clr
                else:
                    clr = back_clr
                text = font.render(word, True, txt_clr, clr)

                txt_w = text.get_width()
                pos[0] += txt_w//2

                textRect = text.get_rect()
                textRect.center = tuple(pos)
                win.blit(text, textRect)
                pos[0] += txt_w//2 + 10 

            pos[0] = 15
            pos[1] += 45

        pygame.display.flip()


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock = pygame.time.Clock()
        clock.tick(fps)

        draw(win, high_word, high_sentence)
        
        try:
            if current_time + 1 < time() and high_word > len(sentece_list[s].split(' ')) - 1:
                high_word = 0
                s += 1
                high_sentence += 1
                current_time = time()

            if current_time + 0.35 < time() and not high_word > len(sentece_list[s].split(' ')) - 1:
                high_word += 1
                current_time = time()

        except IndexError:
            run = False
    
    sleep(1)
    pygame.quit()


Thread(target = narrate).start() 
Thread(target = display).start()