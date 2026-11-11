from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from sparrow import Sparrow

boy = None
sparrows = []


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy, sparrows

    boy = Boy()
    game_world.add_oject(boy)

    sparrows = [Sparrow(index) for index in range(10)]
    for sparrow in sparrows:
        game_world.add_oject(sparrow)

    grass = Grass()
    game_world.add_oject(grass, 0)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy, sparrows
    game_world.clear()
    boy = None
    sparrows = []


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()






