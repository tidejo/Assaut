import pyglet

# Create a window
window = pyglet.window.Window(width=800, height=600)

# Define the size of the map
map_width = 2000
map_height = 2000

# Define the viewport
viewport_width = 400
viewport_height = 300

# Player position
player_x = map_width // 2
player_y = map_height // 2

# Update function to handle player movement and viewport update
def update(dt):
    global player_x, player_y
    # Simulate player movement (replace with actual input handling)
    player_x += 1
    player_y += 1
    # Update viewport position to keep the player centered
    viewport_x = max(0, min(player_x - viewport_width // 2, map_width - viewport_width))
    viewport_y = max(0, min(player_y - viewport_height // 2, map_height - viewport_height))
    # Set viewport
    pyglet.gl.glViewport(viewport_x, viewport_y, viewport_width, viewport_height)

# Draw function to render the map
@window.event
def on_draw():
    window.clear()
    # Draw the visible portion of the map (replace with actual rendering code)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', [0, 0, 0, map_height, map_width, map_height, map_width, 0]))

# Schedule the update function
pyglet.clock.schedule_interval(update, 1/60)

# Run the application
pyglet.app.run()
