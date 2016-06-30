# Mini-project 4 for Principles of Computing class

# based on the template from: http://www.codeskulptor.org/#poc_zombie_template.py

"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


def mniejsza(num_x,num_y):
    """
    helper function, return smaller of two numbers
    """
    if num_x < num_y:
        return num_x
    else:
        return num_y

class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for item in self._zombie_list:
            yield item
        
    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        iloczyn = self._grid_height * self._grid_width
        if entity_type == ZOMBIE:
            visited = poc_grid.Grid(self._grid_height, self._grid_width)
            distance_field = [[iloczyn for dummy_col in range(self._grid_width)] 
                              for dummy_row in range(self._grid_height)]
            boundary  = poc_queue.Queue()
            for item in self.zombies():
                boundary.enqueue(item)
            for item in boundary:
                visited.set_full(item[0], item[1])
                distance_field[item[0]][item[1]] = 0
            while boundary:   
                cell = boundary.dequeue()
                neighbors = self.four_neighbors(cell[0], cell[1])
                for neighbor in neighbors:
                    if self.is_empty(neighbor[0], neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] = mniejsza(1 + distance_field[cell[0]][cell[1]], distance_field[neighbor[0]][neighbor[1]])
            return distance_field            
        else:
            visited = poc_grid.Grid(self._grid_height, self._grid_width)
            distance_field = [[iloczyn for dummy_col in range(self._grid_width)] 
                              for dummy_row in range(self._grid_height)]
            boundary  = poc_queue.Queue()
            for item in self.humans():
                boundary.enqueue(item)
            for item in boundary:
                visited.set_full(item[0], item[1])
                distance_field[item[0]][item[1]] = 0
            while boundary:   
                cell = boundary.dequeue()
                neighbors = self.four_neighbors(cell[0], cell[1])
                for neighbor in neighbors:
                    if self.is_empty(neighbor[0], neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] = mniejsza(1 + distance_field[cell[0]][cell[1]], distance_field[neighbor[0]][neighbor[1]])
            return distance_field
    
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        b_list = [[i,self._human_list[i]] for i in range(len(self._human_list))]
        for item in b_list:
            points = []
            cell = (item[1][0], item[1][1])
            points = self.eight_neighbors(cell[0], cell[1])
            points.append(cell)
            points_passable = [point for point in points if self.is_empty(point[0], point[1])]
            dists = [zombie_distance[point[0]][point[1]] for point in points_passable]
            dists_max_dist = max(dists)
            dists_max_points = [point for point in points_passable if zombie_distance[point[0]][point[1]]==dists_max_dist]
            new_item = random.choice(dists_max_points)
            self._human_list[item[0]] = new_item

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        b_list = [[i,self._zombie_list[i]] for i in range(len(self._zombie_list))]
        for item in b_list:
            points = []
            cell = (item[1][0], item[1][1])
            points = self.four_neighbors(cell[0], cell[1])
            points.append(cell)
            points_passable = [point for point in points if self.is_empty(point[0], point[1])]
            dists = [human_distance[point[0]][point[1]] for point in points_passable]
            dists_min_dist = min(dists)
            dists_min_points = [point for point in points_passable if human_distance[point[0]][point[1]]==dists_min_dist]
            new_item = random.choice(dists_min_points)
            self._zombie_list[item[0]] = new_item


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(40, 30))
