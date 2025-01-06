import pgzrun
import pygame
from random import randint

WIDTH = 800
HEIGHT = 600

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100

ballon = Actor("balloon")
ballon.pos = 400, 300

vogel = Actor("bird-up")
vogel.pos = randint(800, 1600), randint(10, 200)

huis = Actor("house")
huis.pos = randint(800, 1600), 460

boom = Actor("tree")
boom.pos = randint(800, 1600), 450

button_rect = Rect(
    ((WIDTH - BUTTON_WIDTH) // 2, (HEIGHT - BUTTON_HEIGHT) // 2),  # X, Y (centraal)
    (BUTTON_WIDTH, BUTTON_HEIGHT)                                 # Breedte, hoogte
)

vogel_omhoog = True
omhoog = False
game_over = False
title_set = False
game_started = False
score = 0
aantal_updates = 0

scores = []

def update_hoogste_scores():
    global score, scores
    bestandsnaam = 'hoogste-scores.txt'
    scores = []
    with open(bestandsnaam, 'r') as bestand:
        lijn = bestand.readline()
        hoogste_scores = lijn.split()
        for hoogste_score in hoogste_scores:
            if(score > int(hoogste_score)):
                scores.append(str(score) + ' ')
                score = int(hoogste_score)
            else:
                scores.append(str(hoogste_score) + ' ')
        with open(bestandsnaam, 'w') as bestand:
            for hoogste_score in scores:
                bestand.write(hoogste_score)

def toon_hoogste_scores():
    screen.draw.text('HOOGSTE SCORES', (350, 150), color='black')
    y = 175
    positie = 1
    for hoogste_score in scores:
        screen.draw.text(str(positie) + '. ' + hoogste_score, (350, y), color='black')
        y += 25
        positie += 1

def draw():
    screen.blit("background", (0, 0))
    if not game_started:
        screen.draw.filled_rect(button_rect, "green")
        screen.draw.text(
            "START",
            center=button_rect.center,
            fontsize=50,
            color="white"
        )
    elif not game_over and game_started:
        ballon.draw()
        vogel.draw()
        huis.draw()
        boom.draw()
        screen.draw.text('Score: ' + str(score), (700, 5), color='black')
    else:
        toon_hoogste_scores()

def on_mouse_down(pos):
    global omhoog, game_started
    if button_rect.collidepoint(pos) and not game_started:
        game_started = True
    else:
        omhoog = True
        ballon.y -= 50

def on_mouse_up():
    global omhoog
    omhoog = False

def fladder():
    global vogel_omhoog
    if vogel_omhoog:
        vogel.image = 'bird-down'
        vogel_omhoog = False
    else:
        vogel.image = 'bird-up'
        vogel_omhoog = True

def update():
    global game_over, score, aantal_updates, title_set, game_started
    if not game_over and game_started:
        if not omhoog:
            ballon.y += 1

        if vogel.x > 0:
            vogel.x -= 4
            if aantal_updates == 9:
                fladder()
                aantal_updates = 0
            else:
                aantal_updates += 1
        else:
            vogel.x = randint(800, 1600)
            vogel.y = randint(10, 200)
            score += 1
            aantal_updates = 0

        if huis.right > 0:
            huis.x -= 2
        else:
            huis.x = randint(800, 1600)
            score += 1

        if boom.right > 0:
            boom.x -= 2
        else:
            boom.x = randint(800, 1600)
            score += 1

        if ballon.top < 0 or ballon.bottom > 560:
            game_over = True
            update_hoogste_scores()

        if ballon.collidepoint(vogel.x, vogel.y) or \
           ballon.collidepoint(huis.x, huis.y) or \
           ballon.collidepoint(boom.x, boom.y):
                game_over = True
                update_hoogste_scores()

    if not title_set:
        pygame.display.set_caption("Luchtballon")
        title_set = True

pgzrun.go()