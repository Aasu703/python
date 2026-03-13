import pygame # importing the pygame library to create a graphical simulation of planets orbiting around a star.
import math 
pygame.init() # initializing the pygame library to set up the simulation environment.

WIDTH, HEIGHT = 800, 800 # defining the width and height of the simulation window in pixels. 
# The window will be 800 pixels wide and 800 pixels tall.
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a window for the simulation using the defined width and height.
pygame.display.set_caption("Planet Simulation") # setting the caption of the window to "Planet Simulation" to indicate the purpose of the simulation. 

WHITE = (255, 255, 255) 


class Planet:
    AU = 149.6e6 * 1000 # defining a constant for the astronomical unit (AU) in meters, which is the average distance from the Earth to the Sun.
    G = 6.67428e-11 # defining a constant for the gravitational constant in m^3 kg^-1 s^-2, which is used to calculate the gravitational force between two objects.
    SCALE = 250 / AU # defining a scale factor to convert the distance from meters to pixels for the simulation.
    TIMESTEP = 3600 * 24 # defining a time step for the simulation in seconds, which represents one day in the simulation.

    def __init__(self, x, y, radius, color, mass): # defining the constructor method for the Planet class, 
                                                # which initializes the attributes of a planet object.
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0 
    
    def draw(self, win):
        x=self.x * self.SCALE + WIDTH / 2 # calculating the x-coordinate of the planet on the simulation window by scaling its position and centering it.
        y=self.y * self.SCALE + HEIGHT / 2 # calculating the y-coordinate of the planet on the simulation window by scaling its position and centering it.
        pygame.draw.circle(win, self.color, (x, y), self.radius) # drawing a circle on the simulation window to represent the planet, using its color, calculated position, and radius.

def main():
    run = True
    clock = pygame.time.Clock() # creating a clock object to control the frame rate of the simulation.
    while run:
        clock.tick(60) # limiting the frame rate to 60 frames per second.
        WIN.fill(WHITE)
        pygame.display.update() # updating the display to reflect any changes made to the simulation window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit() # quitting the pygame library and closing the simulation window when the main loop ends.

main() # calling the main function to start the simulation. 