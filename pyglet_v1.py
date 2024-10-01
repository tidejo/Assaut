import pyglet
from pyglet import shapes
import time
import random
import math
from pyglet import image
from pyglet.image.codecs.png import PNGImageDecoder

START_TIME = time.time()
PI = math.pi
SPRITE_SCALE = 0.3
WIDTH = 1000
HEIGHT = 800

music = pyglet.resource.media('sounds/background_music/penis_music.wav')
gunshot_sound = pyglet.resource.media('sounds/sound_fx/gunshot.wav', streaming=False)
collision_sound = pyglet.resource.media('sounds/sound_fx/bonk.wav', streaming=False)
music.play()

ufo1 = image.load('sprites/ufo-1.png', decoder=PNGImageDecoder())
ufo2 = image.load('sprites/ufo-2.png', decoder=PNGImageDecoder())

ufo_width = ufo1.width
ufo_height = ufo1.height


key_states = {  # Dict which sets key states
    pyglet.window.key.W: False,
    pyglet.window.key.S: False,
    pyglet.window.key.A: False,
    pyglet.window.key.D: False,
    pyglet.window.key.SPACE: False,
    pyglet.window.key.UP: False,
    pyglet.window.key.DOWN: False,
    pyglet.window.key.LEFT: False,
    pyglet.window.key.RIGHT: False,
    pyglet.window.key.SLASH: False,
}

mouse = [0, 0]


class Player:
    """Creates player class"""
    def __init__(self, id, x, y, color):
        self.id = id
        self.position = [x, y]
        self.velocity = [0, 0]
        self.thrust = 0.1
        self.mass = 50
        self.width = ufo_width
        self.height = ufo_height
        self.color = color
        self.health = 100
        self.last_shot = 0
    
    def draw(self):
        if self.id == 1:
            ufo1.blit(self.position[0]-(self.width/2), self.position[1]-(self.height/2))
        elif self.id == 2:
            ufo2.blit(self.position[0]-(self.width/2), self.position[1]-(self.height/2))
    
    def accelerate(self, dir):
        self.velocity[0] += self.thrust * math.cos(dir)
        self.velocity[1] += self.thrust * math.sin(dir)

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def shot(self):
        self.last_shot = time.time()

class Obstacle:
    """Class wich spawns obstacles for the players to move around"""
    def __init__(self):
        self.width = random.randint(10,30)
        self.height = random.randint(10,30)
        self.position = [random.randint(100,WIDTH - 100), random.randint(100,HEIGHT - 100)]
        self.velocity = [0,0]
        self.mass = self.width * self.height / 20
        self.color = (255,255,255)
    
    def draw(self):
        shapes.Rectangle(self.position[0] - self.width /2, self.position[1] - self.height/2, self.width / 2, self.height/2, color=self.color).draw()
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

class Projectile:
    def __init__(self, p, v):
        self.width = random.randint(10,10)
        self.height = random.randint(10,10)
        self.damage = 50
        self.position = [p[0],p[1]]
        self.velocity = [v[0],v[1]]
        self.color = (0, 255, 0)
    
    def draw(self):
        shapes.Rectangle(self.position[0] - self.width /2, self.position[1] - self.height/2, self.width / 2, self.height/2, color=self.color).draw()
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

# Function to display text at the appropiate times without having to define it in the on_draw() function
def display_text():
    opening_text = pyglet.text.Label('Welkom bij de super mega assaut game',font_name='Times New Roman',font_size=26,x=window.width//2, y=window.height-100,anchor_x='center', anchor_y='center')
    explanation_game = pyglet.text.Label('Jullie doel is om elkaar kapot te maken',font_name='Times New Roman',font_size=26,x=window.width//2, y=window.height-100,anchor_x='center', anchor_y='center')
    tijn_dikke_flikker = pyglet.text.Label('Mind you dat ik dit aan het typen ben terwijl Tijn lekker ligt te ronken met zijn dikke reet. Kaulo hoertje.',font_name='Times New Roman',font_size=16,x=window.width//2, y=window.height-100,anchor_x='center', anchor_y='center')

    if not time.time() > START_TIME + 3:
        return opening_text.draw()
    elif time.time() > START_TIME+3 and not time.time() > START_TIME+6:
        return explanation_game.draw()
    elif time.time() > START_TIME+6 and not time.time() > START_TIME+14:
        return tijn_dikke_flikker.draw()
    

# If two objects hit each other simulate their collision based on their mass and velocity
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

        collision_sound.play()

# If player and projectile are at the same spot player is hit and projectile is removed
def hit(player, projectile):
    if abs(player.position[0] - projectile.position[0]) <= (player.width/2 + projectile.width/2) and abs(player.position[1] - projectile.position[1]) <= (player.height/2 + projectile.height/2):
        player.health -= projectile.damage
        projectiles.remove(projectile)

# If player presses shoot, shoot a projectile aiming in direction of the mouse, but adding the players own velocity
def shoot(gunner, projectiles, mouse):
    if len(projectiles) > 20:
        del projectiles[0]

    v_projectile = 5

    dx = mouse[0] - gunner.position[0]
    dy = mouse[1] - gunner.position[1]

    vl = math.sqrt(dx**2 + dy**2)

    v = [((dx*v_projectile)/vl) + gunner.velocity[0], ((dy*v_projectile)/vl) + gunner.velocity[1]]
    p = gunner.position.copy()
    if abs(v[0]) > abs(v[1]):    
        p[0] += (v[0] / abs(v[0])) * (gunner.width/1.5)
    else:
        p[1] += (v[1] / abs(v[1])) * (gunner.height/1.5)
    projectiles.append(Projectile(p, v))
    gunshot_sound.play()
    return projectiles


def update(dt): 
    global game_over, winner
# Movement commands player 1         
    if key_states[pyglet.window.key.D]:
        player1.accelerate(0)
    if key_states[pyglet.window.key.W]:
        player1.accelerate(0.5*PI)
    if key_states[pyglet.window.key.A]:
        player1.accelerate(PI)
    if key_states[pyglet.window.key.S]:
        player1.accelerate(1.5*PI)
# Movement commands player 2
    if key_states[pyglet.window.key.RIGHT]:
        player2.accelerate(0)
    if key_states[pyglet.window.key.UP]:
        player2.accelerate(0.5*PI)
    if key_states[pyglet.window.key.LEFT]:
        player2.accelerate(PI)
    if key_states[pyglet.window.key.DOWN]:
        player2.accelerate(1.5*PI)
# Shooting commands
    if key_states[pyglet.window.key.SPACE] and (time.time() - player1.last_shot) > 1:
        shoot(player1, projectiles, mouse)
        player1.shot()
    if key_states[pyglet.window.key.SLASH] and (time.time() - player2.last_shot) > 1:
        shoot(player2, projectiles, mouse)
        player2.shot()
        
    player1.move()
    player2.move()
    for obstacle in obstacles:
        obstacle.move()
        collision(player1, obstacle)
        collision(player2, obstacle)

    for projectile in projectiles:
        hit(player1, projectile)
        hit(player2, projectile)
        projectile.move()

    collision(player1, player2)

    if player1.health <= 0:
        game_over = True
        winner = player2
    elif player2.health <= 0:
        game_over = True
        winner = player1

window = pyglet.window.Window(WIDTH, HEIGHT)
batch = pyglet.graphics.Batch()

player1 = Player(1, 150, 240, (255, 0, 0))  # (id, start x, start y, color)
player2 = Player(2, 250, 240, (0, 0, 255))

number_of_obstacles = random.randint(5,10)
obstacles = []
for i in range(number_of_obstacles):
    obstacles.append(Obstacle())

projectiles = []

game_over = False
winner = None

@window.event
def on_key_press(symbol, modifiers):
    if symbol in key_states:
        key_states[symbol] = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol in key_states:
        key_states[symbol] = False

@window.event
def on_mouse_motion(mouse_x, mouse_y, mouse_dx, mouse_dy):
    mouse[0] = mouse_x
    mouse[1] = mouse_y
    pass

@window.event
def on_draw():
    if not game_over:
        window.clear()
        display_text()
        player1.draw()
        player2.draw()
        for obstacle in obstacles:
            obstacle.draw()
        for projectile in projectiles:
            projectile.draw()
    else:
        label = pyglet.text.Label(f"GAME OVER\nPlayer {winner.id} has won!",font_name='Times New Roman',font_size=36,x=window.width//2, y=window.height//2,anchor_x='center', anchor_y='center')
        label.draw()

# Schedules the update function to be called every frame
pyglet.clock.schedule_interval(update, 1/144.0)
pyglet.app.run()