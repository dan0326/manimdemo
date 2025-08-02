from manimlib import *

class Block:
    def __init__(self, position, mass):
        self.position = position
        self.square = Square(color= BLUE)
        self.square.move_to(position)
        self.mass = mass

    @property
    def current_position(self):
        """Get current position from the square"""
        return self.square.get_center()
    



class blocksCollision(Scene):
    def construct(self):
        # Setup floor and wall
        
        # Create the floor - a horizontal line at the bottom
        floor_y = -3.5  # Position the floor near bottom of screen
        floor_start = np.array([-7, floor_y, 0])
        floor_end = np.array([15, floor_y, 0])
        floor = Line(floor_start, floor_end, color=WHITE, stroke_width=6)
        self.frame.set_height(13)
        
        # Create the wall - a vertical line on the left side
        wall_x = -6
        wall_start = np.array([wall_x, floor_y, 0])
        wall_end = np.array([wall_x, 4, 0])
        wall = Line(wall_start, wall_end, color=WHITE, stroke_width=6)
        self.add(floor, wall)
        floor_label = Text("Floor", font_size=24).next_to(floor, DOWN, buff=0.2)
        wall_label = Text("Wall", font_size=24).next_to(wall, LEFT, buff=0.2)
        self.add(floor_label, wall_label)
        # Store positions for collision detection
        self.floor_y = floor_y
        self.wall_x = wall_x

        #add block
        obj1 = Block(position=[6, floor_y+1, 0], mass =10)
        self.add(obj1.square)
        path1 = Line(np.array([6, floor_y+1, 0]), np.array([-5, floor_y+1, 0]))
        self.play(MoveAlongPath(obj1.square, path=path1), rate_func=linear, run_time=2)
        obj1.current_position
        
        
