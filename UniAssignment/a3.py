"""
CSSE1001 Assignment 3
Semester 2, 2020
"""
import tkinter as tk
from PIL import ImageTk, Image

__author__ = "{{Oskar Duce}} ({{45854437}})"
__email__ = "o.duce@uqconnect.edu.au"
__date__ = "23/10/2020"

# ~~~~~~~~~~~~~~~~~  Constants  ~~~~~~~~~~~~~~~~~

GAME_LEVELS = {
    "game1.txt": 7,     
    "game2.txt": 12,    
    "game3.txt": 19,
}

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {
    "w": (-1, 0),
    "s": (1, 0),
    "d": (0, 1),
    "a": (0, -1)
}

WIN_TEXT = "You have won the game with your strength and honour!"

LOSE_TEXT = "You have lost all your strength and honour."

TASK_ONE = 1
TASK_TWO = 2

TASK_TWO_END_TEXT1 = "You have finished the level with a score of "
TASK_TWO_END_TEXT2 = "Would you like to play again?"

QUIT = "Do you want to quit?"

TITLE = "Key Cave Adventure Game"


# ~~~~~~~~~~~~~~~~~  Classes  ~~~~~~~~~~~~~~~~~

class Entity:
    """Entity in the dungeon."""
    def __init__(self):
        """Constructs an entity."""
        self._entity_id = 'Entity'
        self._collision_state = True

    def get_id(self):
        """Returns the id on the entity. (str)"""
        return self._entity_id

    def set_collide(self, collidable):
        """Sets the collision state of the entity.
            
        Parameters:
            collidable (bool): True or False.
        """
        self._collision_state = collidable

    def can_collide(self):
        """Returns whether the entity can be collided with. (bool)"""
        if self._collision_state is True:
            return True
        else:
            return False

    def __str__(self):
        return "Entity('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)


class Wall(Entity):
    """Wall of the dungeon. (Entity)"""
    def __init__(self):
        """Constructs a wall."""
        self._entity_id = WALL
        super().set_collide(False)
        
    def __str__(self):
        return "Wall('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)

    
class Item(Entity):
    """Item in the dungeon. (Entity)"""
    def __init__(self):
        """Constructs an Item."""
        super().set_collide(True)
        self._entity_id = 'Entity'

    def on_hit(self, game):
        """What happens when a player and item collide.
            
        Parameters:
            game (GameLogic): Current game.
        """
        raise NotImplementedError

    def __str__(self):
        return "Item('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)

    
class Key(Item):
    """Key in the dungeon. (Item)"""
    def __init__(self):
        """Constructs a Key."""
        self._entity_id = KEY
        super().set_collide(True)

    def __str__(self):
        return "Key('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)

    def on_hit(self, game):
        """What happens when a player and Key collide.
            
        Parameters:
            game (GameLogic): Current game.
        """
        game.get_game_information().pop(game.get_player().get_position())
        game.get_player().add_item(self)            
    
class MoveIncrease(Item):
    """MoveIncrease in the dungeon. (Item)"""
    def __init__(self, moves = 5):
        """Constructs a MoveIncrease."""
        self._entity_id = MOVE_INCREASE
        self._move_increase_amount = moves
        super().set_collide(True)

    def __str__(self):
        return "MoveIncrease('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)

    def on_hit(self, game):
        """What happens when a player and MoveIncrease collide.
            
        Parameters:
            game (GameLogic): Current game.
        """
        game.get_game_information().pop(game.get_player().get_position())
        game.get_player().change_move_count(self._move_increase_amount)


class Door(Entity):
    """Door in the dungeon. (Entity)"""
    def __init__(self):
        """Constructs a Door."""
        super().set_collide(True)
        self._entity_id = DOOR

    def __str__(self):
        return "Door('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)

    def on_hit(self, game):
        """What happens when a player and Door collide.
            
        Parameters:
            game (GameLogic): Current game.
        """
        for item in game.get_player().get_inventory():
            if item.get_id() == KEY:
                game.set_win(True)
                return

        print("You don't have the key!")

    
class Player(Entity):
    """Player in the dungeon. (Entity)"""
    def __init__(self, move_count):
        """Constructs the player.

        Parameters:
            move_count (int): How many moves the player is given.
        """
        self._move_count = move_count
        self._inventory = []
        self._position = None
        super().set_collide(True)
        self._entity_id = PLAYER

    def set_position(self, position):
        """Sets the position of the player.

        Parameters:
            position (tuple<int, int>): Position in the dungeon.
        """
        self._position = position

    def get_position(self):
        """Returns the position of the player. (tuple<int, int>)"""
        return self._position

    def change_move_count(self, number):
        """Adds moves to the move count.

        Parameters:
            number (int): Amount of moves.
        """
        self._move_count += number

    def set_move_count(self, move_count):
        self._move_count = move_count

    def moves_remaining(self):
        """Returns the move count of the player. (int)"""
        return self._move_count

    def add_item(self, item):
        """Adds an item to the player's inventory.

        Parameters:
            item (Entity): An item in the dungeon.
        """
        self._inventory += [item]

    def get_inventory(self):
        """Returns the inventoy of the player. (list)"""
        return self._inventory

    def __str__(self):
        return "Player('{}')".format(self._entity_id)

    def __repr__(self):
        return str(self)


def load_game(filename):
    """Create a 2D array of string representing the dungeon to display.
    
    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the 
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)
    
    return dungeon_layout


class GameLogic:
    """Current game."""
    def __init__(self, dungeon_name='game2.txt'):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            (list<tuple<int, int>>): List of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions

    def get_dungeon_size(self):
        """Returns the size of the dungeon. (int)"""
        return self._dungeon_size

    def init_game_information(self):
        """Initializes the game information.

        Returns:
            (dict<tuple<int, int>: Entity>): The information of the game including position and entity.
        """
        self.get_player().set_position(self.get_positions(PLAYER)[0])
        
        game_information = {}
        game_information[self.get_positions(KEY)[0]] = Key()
        game_information[self.get_positions(DOOR)[0]] = Door()
        
        for i in range(len(self.get_positions(WALL))):
            game_information[self.get_positions(WALL)[i]] = Wall()
            
        if len(self.get_positions(MOVE_INCREASE)) != 0:
            game_information[self.get_positions(MOVE_INCREASE)[0]] = MoveIncrease()
            
        return game_information

    def get_game_information(self):
        """Returns game information. (dict<tuple<int, int>: Entity>)"""
        return self._game_information

    def set_game_information(self, information):
        self._game_information = information

    def get_player(self):
        """Returns the player. (Player)"""
        return self._player

    def get_entity(self, position):
        """ Returns an entity in a position.

        Parameters:
            position (<tuple<int, int>): The position in the dungeon.

        Returns:
            (Entity): An entity in the dungeon.
        """
        try:
            return self._game_information[position]
        except:
            return None


    def get_entity_in_direction(self, direction):
        """ Returns an entity in a direction from the players position.

        Parameters:
            direction (str): W, S, D or A representing up, down, right and left respectively.

        Returns:
            (Entity): An entity in the dungeon.
        """
        position_in_direction = []
        for i in range(2):
            position_in_direction.append(self._player.get_position()[i]+DIRECTIONS[direction][i])
        return self.get_entity(tuple(position_in_direction))
        

    def collision_check(self, direction):
        """Returns True if the entity in the direction can't be collided with.

        Parameters:
            direction (str): W, S, D or A representing up, down, right and left respectively.

        Returns:
            (bool): True or False.
        """
        if self.get_entity_in_direction(direction) == None:
            return False
        elif self.get_entity_in_direction(direction).can_collide() is True:
            return False
        else:
            return True

    def new_position(self, direction):
        """Returns position in a given direction from the player.

        Parameters:
            direction (str): W, S, D or A representing up, down, right and left respectively.

        Returns:
            (<tuple<int, int>): The position in the dungeon.
        """
        position_in_direction = []
        
        for i in range(2):
            position_in_direction.append(self._player.get_position()[i]+DIRECTIONS[direction][i])

        return tuple(position_in_direction)

    def move_player(self, direction):
        """Sets the players position to a position in a given direction.

        Parameters:
            direction (str): W, S, D or A representing up, down, right and left respectively.
        """
        self._player.set_position(self.new_position(direction))

    def check_game_over(self):
        """Returns True if the game is over. (bool)"""
        if self.get_player().moves_remaining() == 0:
            return True
        else:
            return False

    def set_win(self, win):
        """Sets the game state to True if game is won.

        Parameters:
            win (bool): True or False.
        """
        self._win = win

    def won(self):
        """Returns the True if the game is won."""
        return self._win


# ~~~~~~~~~~~~~~~~~  View Classes  ~~~~~~~~~~~~~~~~~

class AbstractGrid(tk.Canvas):
    def get_bbox(self, position):
        """Returns the bounding box for the (row, col) position.
    
        Parameters:
            position (tuple): The position of the box (row, coloumn)

        Returns:
            bbox (tuple): 2 coordinates of the top left and bottom right
                                corners of the box. (x1, y1, x2, y2)
        """
        bbox = (self._width_scale_ratio*position[1], self._height_scale_ratio*position[0], self._width_scale_ratio*(position[1]+1), self._height_scale_ratio*(position[0]+1))
        return bbox

    def pixel_to_position(self, pixel):
        """ Converts  the  x,  y  pixel  position (in  graphics  units)
            to  a  (row,  col) position.
    
        Parameters:
            pixel (tuple): (x,y) Coordinate

        Returns:
            position (tuple): (row, coloumn) Coordinate
        """
        position = (pixel[1]//self._height_scale_ratio, pixel[0]//self._width_scale_ratio)
        return position

    def get_position_centre(self, position):
        """ Gets  the  graphics  coordinates  for  the  center
            of  the  cell  at  thegiven (row, col) position.
    
        Parameters:
            position (tuple): (row, coloumn) Coordinate

        Returns:
            pixel (tuple): (x,y) Coordinate
        """
        position = (self._width_scale_ratio*(position[1]+.5), self._height_scale_ratio*(position[0]+.5))
        return position

    def annotate_position(self, position, text):
        """ Annotates the cell at the given (row, col)
            position with the provided text.
    
        Parameters:
            position (tuple): (row, coloumn) Coordinate
            text (str): text that inserted into box
        """
        self.create_text(position, text=text)


class DungeonMap(AbstractGrid):
    """Map of the Dungeon"""
    def __init__(self, master, size, width=600, **kwargs):
        """Constructs the Dungeon Map."""
        self._size = size
        self._width = width
        self._height = width
        self._width_scale_ratio = self._width/self._size
        self._height_scale_ratio = self._height/self._size
        
        self._canvas_map = AbstractGrid(master)
        self._canvas_map.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._canvas_map.configure(width=self._width, height=self._width)
        
        
    def draw_grid(self, game, player_position):
        """ Draws the dungeon on the Dungeon Map based on dungeon,
            and draws the player at the specified (row, col) position.
    
        Parameters:
            game (GameLogic): The game being played
            player_position (tuple): (row, coloumn) Coordinate of player
        """
        temp_colour = ''
        temp_name = ''
        self._canvas_map.delete(tk.ALL)
        
        for key in game._game_information:
            if str(game._game_information[key]) == str(Key()):
                temp_colour = 'yellow'
                temp_name = 'Trash'
            elif str(game._game_information[key]) == str(Wall()):
                temp_colour = 'dark grey'
                temp_name = ''
            elif str(game._game_information[key]) == str(Door()):
                temp_colour = 'red'
                temp_name = 'Nest'
            elif str(game._game_information[key]) == str(MoveIncrease()):
                temp_colour = 'orange'
                temp_name = 'Banana'
                
            self._canvas_map.create_rectangle(self.get_bbox(key), fill=temp_colour)
            self._canvas_map.annotate_position(self.get_position_centre(key), temp_name)

        self._canvas_map.create_rectangle(self.get_bbox(player_position), fill='medium spring green')
        self._canvas_map.annotate_position(self.get_position_centre(player_position), 'Ibis')


class AdvancedDungeonMap(AbstractGrid):
    """Advanced Map of the Dungeon"""
    def __init__(self, master, size, width=600, **kwargs):
        """Constructs the Advanced Dungeon Map."""
        self._size = size
        self._width = width
        self._height = width
        self._width_scale_ratio = self._width/self._size
        self._height_scale_ratio = self._height/self._size

        self._canvas_map = AbstractGrid(master)
        self._canvas_map.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._canvas_map.configure(width=self._width, height=self._width)
        
    def draw_grid(self, dungeon, player_position):
        """ Draws the dungeon on the Advanced Dungeon Map based on dungeon,
            and draws the player at the specified (row, col) position.
    
        Parameters:
            game (GameLogic): The game being played
            player_position (tuple): (row, coloumn) Coordinate of player
        """
        self._canvas_map.delete(tk.ALL)

        img = Image.open("images\empty.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._empty = ImageTk.PhotoImage(img)
        for row in range(self._size):
            for column in range(self._size):
                self._canvas_map.create_image((self._width_scale_ratio*row, self._width_scale_ratio*column), image=self._empty, anchor=tk.NW)
        
        img = Image.open("images\key.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._key = ImageTk.PhotoImage(img)
        
        img = Image.open("images\wall.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._wall = ImageTk.PhotoImage(img)
        
        img = Image.open("images\door.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._door = ImageTk.PhotoImage(img)
        
        img = Image.open("images\moveIncrease.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._moveIncrease = ImageTk.PhotoImage(img)
        
        for key in dungeon._game_information:
            if str(dungeon._game_information[key]) == str(Key()):
                self._canvas_map.create_image(self.get_bbox(key)[0:2], image=self._key, anchor=tk.NW)
            elif str(dungeon._game_information[key]) == str(Wall()):
                self._canvas_map.create_image(self.get_bbox(key)[0:2], image=self._wall, anchor=tk.NW)
            elif str(dungeon._game_information[key]) == str(Door()):
                self._canvas_map.create_image(self.get_bbox(key)[0:2], image=self._door, anchor=tk.NW)
            elif str(dungeon._game_information[key]) == str(MoveIncrease()):
                self._canvas_map.create_image(self.get_bbox(key)[0:2], image=self._moveIncrease, anchor=tk.NW)


        img = Image.open("images\player.png")
        img = img.resize((int(self._width_scale_ratio),int(self._height_scale_ratio)))
        self._player = ImageTk.PhotoImage(img)
        self._canvas_map.create_image(self.get_bbox(player_position)[0:2], image=self._player, anchor=tk.NW)


class KeyPad(AbstractGrid):
    """ Keypad: Move controller """
    def __init__(self, master, width=200, height=100, **kwargs):
        """ Contructs the KeyPad """
        self._width = width
        self._height = height
        self._size = 3
        self._width_scale_ratio = self._width/self._size
        self._height_scale_ratio = self._height/self._size
        
        self._canvas_controls = AbstractGrid(master, width=width, height=height)
        self._canvas_controls.pack(side=tk.LEFT, fill=tk.X)
        self._canvas_controls.configure(width=self._width, height=self._height)

        key_pad_dict = {(0,1):'N',(1,0):'W',(1,1):'S',(1,2):'E'}

        for key in key_pad_dict:
            self._canvas_controls.create_rectangle(self.get_bbox(key), fill='dark grey')
            self._canvas_controls.annotate_position(self.get_position_centre(key), key_pad_dict[key])

    def pixel_to_direction(self, pixel):
        """ Converts the x, y pixel position to
            the direction of the arrow depicted at that position.
    
        Parameters:
            pixel (tuple): (x,y) Coordinate

        Returns:
            direction (tuple): Reads pixel to KeyPad and returns direction.
        """
        direction = ''      
        if self.pixel_to_position(pixel) == (0,1):
            direction = 'w'
        elif self.pixel_to_position(pixel) == (1,0):
            direction = 'a'
        elif self.pixel_to_position(pixel) == (1,1):
            direction = 's'
        elif self.pixel_to_position(pixel) == (1,2):
            direction = 'd'
        return direction


class StatusBar(tk.Frame):
    """ Status Bar """
    def __init__(self, master, game, dungeon, dungeon_name, **kwargs):
        """ Contructs the status bar """
        self._master = master
        self._game = game
        self._dungeon = dungeon
        self._dungeon_name = dungeon_name
        
        self._statusbar = tk.Frame(self._master)
        self._statusbar.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self._statusbar_buttons = tk.Frame(self._statusbar)
        self._statusbar_buttons.pack(side=tk.LEFT, fill=tk.X, padx=80)

        self._button_newgame = tk.Button(self._statusbar_buttons, text="New game", command=self.new_game)
        self._button_newgame.pack(side=tk.TOP)
        
        self._button_quit = tk.Button(self._statusbar_buttons, text="Quit", command=self.quit)
        self._button_quit.pack(side=tk.TOP)

        self._statusbar_timer = tk.Frame(self._statusbar)
        self._statusbar_timer.pack(side=tk.LEFT)
        
        img1 = Image.open("images\clock.png")
        img1 = img1.resize((40,50))
        self._hourglass = ImageTk.PhotoImage(img1)
        self._clock = tk.Label(self._statusbar_timer, image = self._hourglass)
        self._clock.pack(side=tk.LEFT)

        self._timer = tk.Label(self._statusbar_timer)
        self._timer.pack(side=tk.LEFT)
        self.reset_timer()
        self.update_clock()

        self._statusbar_movecounter = tk.Frame(self._statusbar)
        self._statusbar_movecounter.pack(side=tk.RIGHT, fill=tk.X, padx=140)

        img2 = Image.open("images\lightning.png")
        img2 = img2.resize((40,50))
        self._lightning_bolt = ImageTk.PhotoImage(img2)
        self._lightning = tk.Label(self._statusbar_movecounter, image = self._lightning_bolt)
        self._lightning.pack(side=tk.LEFT)

        self._movecounter = tk.Label(self._statusbar_movecounter, text="Moves left\n"+str(self._game._player.moves_remaining())+' moves remaining')
        self._movecounter.pack(side=tk.RIGHT)

    def update_clock(self):
        """ Updates the timer on the status bar """
        if not self._stop_timer:
            self._time += 1
            self._timer.configure(text="Time elapsed\n"+str(self._time//60)+'m '+str(self._time%60)+'s')
            self._master.after(1000, self.update_clock)

    def draw_moves(self):
        """ Draws moves onto status bar """
        self._movecounter.config(text="Moves left\n"+str(self._game._player.moves_remaining())+' moves remaining')

    def stop_timer(self):
        """ Stops the status bar timer """
        self._stop_timer = True

    def reset_timer(self):
        """ Resets the status bar timer """
        self._time = -1
        self._stop_timer = False

    def set_time(self, time):
        """ Sets the status bar timer """
        self._time = time

    def get_time(self):
        """ Gets the status bar timer """
        return self._time

    def quit(self):
        """ Asks to quit the game """
        self._popup = tk.Tk()
        self._popup.title(QUIT)
        
        label = tk.Label(self._popup, text=QUIT)
        label.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=10)
        
        buttons_frame = tk.Frame(self._popup)
        buttons_frame.pack(side=tk.TOP, expand=True, fill=tk.X, pady=10)
        
        button1 = tk.Button(buttons_frame, text='Yes', command=self.close)
        button1.pack(side=tk.RIGHT, padx=10, ipadx=20)
        
        button2 = tk.Button(buttons_frame, text='No', command=self._popup.destroy)
        button2.pack(side=tk.RIGHT, padx=10, ipadx=20)
        
        self._popup.mainloop()

    def close(self):
        """ Closes the program """
        self._master.destroy()
        self._popup.destroy()

    def new_game(self):
        """ Restarts the Game """
        self.reset_timer()
        self._game._player = Player(GAME_LEVELS[self._dungeon_name])
        self._game._game_information = self._game.init_game_information()
        self.draw_moves()
        self._dungeon.draw_grid(self._game, self._game._player.get_position())
        

# ~~~~~~~~~~~~~~~~~  Core Game  ~~~~~~~~~~~~~~~~~

class GameApp:
    """Main code of the game."""
    def __init__(self, task=TASK_ONE, dungeon_name="game2.txt"):
        """Constructor of the GameApp class."""
        self._dungeon_name = dungeon_name
        self._game = GameLogic(dungeon_name)
        self._root = tk.Tk()
        self._task = task
        self._reset_game = False
        self.draw()
        self._root.bind('<Key>', self.press)
        self._keypad._canvas_controls.bind('<Button-1>', self.click)
        self._root.mainloop()
        
    def click(self, event):
        """ Reads mouse click """
        try:
            self._move = self._keypad.pixel_to_direction((event.x,event.y))
            self.move()
        except:
            pass
        
    def press(self, event):
        """ Reads keyboard press """
        self._move = event.char
        self.move()

    def move(self):
        """ Moves Player """
        if not self._game.collision_check(self._move):
            self._game.move_player(self._move)
            entity = self._game.get_entity(self._game._player.get_position())
            if entity is not None:
                entity.on_hit(self._game)
            self._dungeon.draw_grid(self._game, self._game._player.get_position())
        self._game._player.change_move_count(-1)

        if self._task == TASK_TWO:
            self._statusbar.draw_moves()
            
        if self._game.check_game_over() or self._game.won():
            if self._task == TASK_ONE:
                
                if self._game.won():
                    text = WIN_TEXT
                    
                elif self._game.check_game_over():
                    text = LOSE_TEXT
                    
                popup = tk.Tk()
                popup.title("Game Over!")
                label = tk.Label(popup, text=text)
                label.pack(fill=tk.BOTH, pady=40, padx=30)
                popup.mainloop()
                
            elif self._task == TASK_TWO:
                
                if self._game.won():
                    title = "You Won!"
                    
                elif self._game.check_game_over():
                    title = "You Lost!"
                    
                self._statusbar.stop_timer()
                
                self._popup = tk.Tk()
                self._popup.title(title)
                
                label1 = tk.Label(self._popup, text=TASK_TWO_END_TEXT1+str(self._statusbar.get_time())+'.')
                label1.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=10)
                
                label2 = tk.Label(self._popup, text=TASK_TWO_END_TEXT2,anchor=tk.NW)
                label2.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
                
                buttons_frame = tk.Frame(self._popup)
                buttons_frame.pack(side=tk.TOP, expand=True, fill=tk.X, pady=10)
                
                button1 = tk.Button(buttons_frame, text='Yes', command=self.new_game)
                button1.pack(side=tk.RIGHT, padx=10, ipadx=20)
                
                button2 = tk.Button(buttons_frame, text='No', command=self.close)
                button2.pack(side=tk.RIGHT, ipadx=20)
                
                self._popup.mainloop()
            

    def draw(self):
        """Draws the game."""
        self._root.title(TITLE)
        
        self._canvas_title = AbstractGrid(self._root)
        self._canvas_title.pack(side=tk.TOP, fill=tk.X)

        self._label_title = tk.Label(self._canvas_title, text=TITLE, font=('Helvetica', 18, 'bold'), bg='medium spring green', pady=10)
        self._label_title.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self._dungeon_keypad_frame = tk.Frame(self._root)
        self._dungeon_keypad_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        if self._task == TASK_ONE:
            self._dungeon = DungeonMap(self._dungeon_keypad_frame, self._game.get_dungeon_size())
        elif self._task == TASK_TWO:
            self._dungeon = AdvancedDungeonMap(self._dungeon_keypad_frame, self._game.get_dungeon_size())
        self._dungeon.draw_grid(self._game, self._game._player.get_position())

        self._keypad = KeyPad(self._dungeon_keypad_frame)
        if self._task == TASK_TWO:
            self._statusbar = StatusBar(self._root, self._game, self._dungeon, self._dungeon_name)
            
            self._menubar = tk.Menu(self._root)
            self._menubar.add_command(label="Save game", command=self.save_game)
            self._menubar.add_command(label="Load game", command=self.load_game)
            self._menubar.add_command(label="New game", command=self.new_game)
            self._menubar.add_command(label="Quit", command=self._statusbar.quit)
            self._root.config(menu=self._menubar)

    def new_game(self):
        """ Restarts the game """
        self._statusbar.reset_timer()
        self._game._player = Player(GAME_LEVELS[self._dungeon_name])
        self._game._game_information = self._game.init_game_information()
        self._statusbar.draw_moves()
        self._dungeon.draw_grid(self._game, self._game._player.get_position())
        
        try:
            self._popup.destroy()
            self._game.set_win(False)
            self._statusbar.update_clock()
        except:
            None

    def close(self):
        """ Closes the program """
        self._root.destroy()
        self._popup.destroy()

    def save_game(self):
        """ Saves the game """
        items = ''
        
        try:
            self._game._game_information[self._game.get_positions(KEY)[0]]
            items += '\n'+str(self._game.get_positions(KEY)[0])
        except:
            items += '\n'+'taken'
            
        try:
            self._game._game_information[self._game.get_positions(MOVE_INCREASE)[0]]
            items += '\n'+str(self._game.get_positions(MOVE_INCREASE)[0])
        except:
            items += '\n'+'taken'
            
        save = open("SavedGame.txt","w")
        save.write(str(self._dungeon_name)+'\n'+str(self._statusbar._time)+'\n'+str(self._game._player.get_position()[0])+'\n'+str(self._game._player.get_position()[1])+'\n'+str(self._game._player.moves_remaining())+items)
        save.close()

    def load_game(self):
        """ Loads the game """
        save = open("SavedGame.txt","r")
        self._information = {}
        count = 1
        
        for line in save:
            self._information[count] = line.strip('\n')
            count += 1
            
        self._game._dungeon = load_game(self._information[1])
        self._game._game_information = self._game.init_game_information()
        self._statusbar.set_time(int(self._information[2]))
        self._game._player.set_position((int(self._information[3]),int(self._information[4])))
        self._game._player.set_move_count(int(self._information[5]))
        
        if self._information[6] == 'taken':
            self._game._player.add_item(Key())
            try:
                self._game.get_game_information().pop(self._game.get_positions(KEY)[0])
            except:
                pass
            
        if self._information[7] == 'taken':
            try:
                self._game.get_game_information().pop(self._game.get_positions(MOVE_INCREASE)[0])
            except:
                pass
            
        self._statusbar.draw_moves()
        self._dungeon.draw_grid(self._game, self._game._player.get_position())
        

if __name__ == "__main__":
    GameApp(TASK_TWO)
