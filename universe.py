#!/usr/bin/python

import pygame as pg
import sys, os

WHITE = (255, 255, 255)

def big_bang(init, screen,
             on_tick=lambda e: e, \
             framerate=28, \
             draw=lambda e: pg.Surface((0,0)), \
             on_key=lambda e, k: e, \
             on_release=lambda e, k: e, \
             ou_mouse=lambda e, x, y, ev: e, \
             stop_when=lambda e: False,\
             debug_mode=False,
             debug_font = 15):

    pg.init()
    state = init
    clock = pg.time.Clock()

    while True:

        pg.display.flip()

        if stop_when(state):
            print(state)
            sys.exit(0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                print(state)
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                state = on_key(state, event.key)
            elif event.type == pg.KEYUP:
                state = on_release(state, event.key)
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION]:
                x, y = pg.mouse.get_pos()
                state = ou_mouse(state, x, y, event.type)

        state = on_tick(state)

        screen.fill(WHITE)
        draw(state)
        if debug_mode:
            print_state(state, screen, debug_font)

        clock.tick(framerate)

def print_state(state, screen, debug_font):
    myfont = pg.font.SysFont("monospace", debug_font)
    # text = str(state).split(',')
    import re
    text = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', str(state))

    counter = debug_font
    for line in text:
        label = myfont.render(line, 1, (255, 0, 0))
        screen.blit(label, (5, counter))
        counter += debug_font