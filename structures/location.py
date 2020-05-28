import pygame
import sys
import random

import math

from walkers.Walker import Walker
import walkers.healthState as h

BLACK = (0, 0, 0)

color = [
    (255, 255, 255), # WHITE
    (255, 50, 50), # RED
    (255, 255, 0), # YELLOW
    (50, 255, 50) # GREEN
    ]

class Location:

    '''
    Attributes
    ----------
    size_x : integer
    size_y : integer
    max_capacity : integer
    walkers : vector of Walkers
    distance_list : vector of pairs of Walkers
    '''


    def __init__(self, size_x, size_y, max_capacity):

        self.size_x = size_x
        self.size_y = size_y
        self.max_capacity = max_capacity

        self.walkers = []
        for i in range(6):
            self.walkers.append([])

        self.no_infected = 0 # number of infected

        # variables for rendering
        self.screen = None
        self.fps = 0
        self.paused = False

    # end __init__


    def enter(self, walker):
        '''
        Make a new Walker enter the Location

        Parameters
        ----------
        walker : Walker
            new walker to enter the location
        '''

        self.walkers[walker.status].append(walker)

    # end enter

    def exit(self, walker):
        '''
        Make a new Walker enter the Location

        Parameters
        ----------
        walker : Walker
            new walker to enter the location
        '''

        self.walkers[walker.status].remove(walker)

    # end exit

    def update(self, virus):
        '''
        update the context inside the location ( a minute (or second, must decide) of life , for each update call)

        Parameters
        ----------
        virus: Virus
            the virus spreading
        '''
        # UPDATE THE POSITION OF EACH WALKER
        for walkerStatus in range(6):
            for walker in self.walkers[walkerStatus]:
                tempx = walker.x + random.randint(-10, 10)
                tempy = walker.y + random.randint(-10, 10)

                tempx = (0 if tempx<0 else (self.size_x if tempx>self.size_x else tempx))
                tempy = (0 if tempy<0 else (self.size_y if tempy>self.size_y else tempy))
                
                walker.move(tempx, tempy)

        # CHECK FOR EACH WALKER IF IT's CLOSE TO AN INFECTED
        #   IF SO -> ROLL

        for susceptible in self.walkers[h.SUSCEPTIBLE]:
            flag = 0

            for asymptomatic in self.walkers[h.ASYMPTOMATIC]:
                if (distance(susceptible, asymptomatic) < virus.range):
                    flag = virus.tryInfection(susceptible)
                    if (flag):
                        break   # non ha senso fare altri controlli
            if not flag:
                for infected in self.walkers[h.INFECTED]:
                    if (distance(susceptible, infected) < virus.range):
                        flag = virus.tryInfection(susceptible)
                        if (flag):
                            break   # non ha senso fare altri controlli
            if flag:
                self.walkers[h.INCUBATION].append(susceptible)
                self.walkers[h.SUSCEPTIBLE].remove(susceptible)

    # end update


    def initRendering(self):
        '''
        Init the rendering engine
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('City')
        self.fps = pygame.time.Clock()
        self.paused = False

    def render(self, virus):
        '''
        render the current situation

        Parameters
        ----------
        virus: Virus
            the virus spreading
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
        if not self.paused:
            self.screen.fill(BLACK)

            font = pygame.font.Font(None, 36)
            
            for walker in self.walkers:
                pygame.draw.circle(self.screen, color[walker.status], (walker.x, walker.y), 5, 0)
                pygame.draw.circle(self.screen, color[walker.status], (walker.x, walker.y), int(virus.range/2), 1)

            pygame.display.update()
            self.fps.tick(30)

# end class Location


def distance(walker1, walker2):
    return math.sqrt((walker2.x - walker1.x)**2 + (walker2.y - walker1.y)**2)
# end distance
