import pyglet
from pyglet import shapes
import time
import random
import math

START_TIME = time.time()
PI = math.pi

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
        self.position = [x, y]
        self.velocity = [0, 0]
        self.thrust = 0.1
        self.mass = 50
        self.width = 50
        self.height = 50
        self.color = color
        self.health = 100
    
    def draw(self):
        shapes.Rectangle(self.position[0] - self.width / 2, self.position[1] - self.height/2, self.width, self.height, color=self.color).draw()
    
    def accelerate(self, dir):
        self.velocity[0] += self.thrust * math.cos(dir)
        self.velocity[1] += self.thrust * math.sin(dir)

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


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
        self.position = [x,y]
        self.velocity = [0,0]
        self.mass = self.width * self.height / 20
        self.color = color
    
    def draw(self):
        shapes.Rectangle(self.position[0] - self.width /2, self.position[1] - self.height/2, self.width / 2, self.height/2, color=self.color).draw()
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


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
    


def collision(object1, object2):
    if abs(object1.position[0] - object2.position[0]) <= (object1.width/2 + object2.width/2) and abs(object1.position[1] - object2.position[1]) <= (object1.height/2 + object2.height/2):
        v1 = object1.velocity.copy()
        v2 = object2.velocity.copy()
        mass_ratio1 = object1.mass/(object1.mass + object2.mass)
        mass_ratio2 = object2.mass/(object1.mass + object2.mass)
        if abs(object1.position[0] - object2.position[0]) >= abs(object1.position[1] - object2.position[1]):
            object1.velocity[0] = object1.velocity[0] - ((v1[0] - v2[0])*mass_ratio2*2)
            object2.velocity[0] = object2.velocity[0] + ((v1[0] - v2[0])*mass_ratio1*2)
        
        if abs(object1.position[0] - object2.position[0]) <= abs(object1.position[1] - object2.position[1]):
            object1.velocity[1] = object1.velocity[1] - ((v1[1] - v2[1])*mass_ratio2*2)
            object2.velocity[1] = object2.velocity[1] + ((v1[1] - v2[1])*mass_ratio1*2)


def update(dt):
    if key_states[pyglet.window.key.D]:
        player1.accelerate(0)
    if key_states[pyglet.window.key.W]:
        player1.accelerate(0.5*PI)
    if key_states[pyglet.window.key.A]:
        player1.accelerate(PI)
    if key_states[pyglet.window.key.S]:
        player1.accelerate(1.5*PI)
    if key_states[pyglet.window.key.RIGHT]:
        player2.accelerate(0)
    if key_states[pyglet.window.key.UP]:
        player2.accelerate(0.5*PI)
    if key_states[pyglet.window.key.LEFT]:
        player2.accelerate(PI)
    if key_states[pyglet.window.key.DOWN]:
        player2.accelerate(1.5*PI)
        
    player1.move()
    player2.move()
    for obstacle in obstacles:
        obstacle.move()
        collision(player1, obstacle)
        collision(player2, obstacle)

    collision(player1, player2)


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
pyglet.clock.schedule_interval(update, 1/144.0)
pyglet.app.run()