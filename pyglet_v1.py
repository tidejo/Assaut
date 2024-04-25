import pyglet
from pyglet import shapes
import time
import random

START_TIME = time.time()

key_states = {  # Dict which sets key states
    pyglet.window.key.W: False,
    pyglet.window.key.S: False,
    pyglet.window.key.A: False,
    pyglet.window.key.D: False,
    pyglet.window.key.UP: False,
    pyglet.window.key.DOWN: False,
    pyglet.window.key.LEFT: False,
    pyglet.window.key.RIGHT: False
}


class Player:
    """Creates player class"""
    def __init__(self, x, y, color):
        self.width = 50
        self.height = 50
        self.rect = shapes.Rectangle(x, y, self.width, self.height, color=color)
        self.speed = 5
        self.health = 100
    
    def draw(self):
        self.rect.draw()
    
    def move_up(self):
        self.rect.y += self.speed
    
    def move_down(self):
        self.rect.y -= self.speed
    
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

class Shot:
    pass

class Powerup_speed:
    pass

class Powerup_health:
    pass

class Powerup_heal:
    pass

class Obstacle:
    """Class wich spawns obstacles for the players to move around"""
    def __init__(self, x, y, color):
        self.width = random.randint(10,30)
        self.height = random.randint(10,30)
        self.rect = shapes.Rectangle(x, y, self.width, self.height, color=color)
    
    def draw(self):
        self.rect.draw()


def display_text():
    """Funtion to display text at the appropiate times 
    without having to define it in the on_draw() function"""
    opening_text = pyglet.text.Label(
    'Welkom bij de super mega assaut game',
    font_name='Times New Roman',
    font_size=26,
    x=window.width//2, y=window.height-100,
    anchor_x='center', anchor_y='center'
    )
    explanation_game = pyglet.text.Label(
    'Jullie doel is om elkaar kappot te maken',
    font_name='Times New Roman',
    font_size=26,
    x=window.width//2, y=window.height-100,
    anchor_x='center', anchor_y='center'
    )
    tijn_dikke_flikker = pyglet.text.Label(
    'Mind you dat ik dit aan het typen ben terwijl Tijn lekker ligt te ronken met zijn dikke reet. Kaulo hoertje.',
    font_name='Times New Roman',
    font_size=16,
    x=window.width//2, y=window.height-100,
    anchor_x='center', anchor_y='center'
    )

    if not time.time() > START_TIME + 3:
        return opening_text.draw()
    if time.time() > START_TIME+3 and not time.time() > START_TIME+6:
        return explanation_game.draw()
    if time.time() > START_TIME+6 and not time.time() > START_TIME+14:
        return tijn_dikke_flikker.draw()


def move(dt):
    if key_states[pyglet.window.key.W]:
        player1.move_up()
    if key_states[pyglet.window.key.S]:
        player1.move_down()
    if key_states[pyglet.window.key.A]:
        player1.move_left()
    if key_states[pyglet.window.key.D]:
        player1.move_right()
    if key_states[pyglet.window.key.UP]:
        player2.move_up()
    if key_states[pyglet.window.key.DOWN]:
        player2.move_down()
    if key_states[pyglet.window.key.LEFT]:
        player2.move_left()
    if key_states[pyglet.window.key.RIGHT]:
        player2.move_right()


window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()

player1 = Player(150, 240, (255, 0, 0))  # (start x, start y, color)
player2 = Player(250, 240, (0, 0, 255))

number_of_obstacles = random.randint(5,10)
obstacles = []
for i in range(number_of_obstacles):
    obstacles.append(Obstacle(random.randint(100,900), random.randint(100,700),(255,255,255)))

@window.event
def on_key_press(symbol, modifiers):
    if symbol in key_states:
        key_states[symbol] = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol in key_states:
        key_states[symbol] = False

@window.event
def on_draw():
    window.clear()
    display_text()
    player1.draw()
    player2.draw()
    for obstacle in obstacles:
        obstacle.draw()

# Schedules the update function to be called every frame
pyglet.clock.schedule_interval(move, 1/60.0)

pyglet.app.run()
