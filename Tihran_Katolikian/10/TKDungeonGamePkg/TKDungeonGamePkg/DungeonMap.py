from DungeonGameMapGenerator import DungeonGameMapGenerator, DungeonCell
from UpdateList import UpdateList
from LoggerDecorator import logger_decorator
import logging
import random


class DungeonMap(UpdateList):

    def __init__(self):
        '''
        Constructor of DungeonMap.
        :param map_size: a size of map;
        :type map_size: int
        '''
        super().__init__()

        self.__init_dicts()
        self.dungeon_map = None
        self.__size = None
        self.__player_position = None
        self.__enemy_position = None

    
    @logger_decorator
    def generate_new_map(self, map_size):
        '''
        Generates a new map.
        :param map_size: a size of map to generate.
        '''
        self.__size = map_size
        self.__generator = DungeonGameMapGenerator()
        self.__player_position, self.dungeon_map = self.__generator.generate_map(map_size)


    @logger_decorator
    def init_from_load(self, player_position, dungeon_map):
        '''
        Inits map from instance.
        :param player_position: a position of player;
        :param dungeon_map: a dungeon map;
        :type player_position: a tuple: (int, int);
        :type dungeon_map: a list of lists of DungeonCells.
        '''
        self.__size = len(dungeon_map)
        self.dungeon_map = dungeon_map
        self.__player_position = player_position


    @logger_decorator
    def __init_dicts(self):
        '''
        Function is used to initialize a dicts that is used for input.
        '''
        self.__hide_everything_except_player_map = {
            DungeonCell.EMPTY : ' ',
            DungeonCell.PLAYER : '*',
            DungeonCell.TRAP: ' ',
            DungeonCell.TREASURE: ' ',
            DungeonCell.ENEMY: 'A'
        }

        self.__output_everything_map = {
            DungeonCell.EMPTY : ' ',
            DungeonCell.PLAYER : '*',
            DungeonCell.TRAP: '#',
            DungeonCell.TREASURE: '$',
            DungeonCell.ENEMY: 'A'
        }


    @logger_decorator
    def __create_map(map_size):
        '''
        Creates a map
        :param map_size: a size of map that will be generated;
        :type map_size: an integer >= 5
        '''


    @logger_decorator
    def get_size(self):
        '''
        The getter method for size of map.
        :return: a size of map;
        :rtype: int.
        '''
        return self.__size

    
    @logger_decorator
    def get_player_position(self):
        '''
        The getter method for position of player.
        :return: a current position of player;
        :rtype: tuple: (int, int).
        '''
        return self.__player_position


    @logger_decorator
    def move_player(self, new_position):
        '''
        Function is used to move player around the map.
        :param new_position: the new position of player;
        :return: a cell on which player will stay after moving;
        :type new_position: tuple: (int, int);
        :rtype: DungeonCell
        '''
        old_x, old_y = self.__player_position
        self.__player_position = new_position
        new_x, new_y = self.__player_position
        previous_cell = self.dungeon_map[new_x][new_y]
        self.dungeon_map[old_x][old_y] = DungeonCell.EMPTY
        self.dungeon_map[new_x][new_y] = DungeonCell.PLAYER
        return previous_cell


    @logger_decorator
    def move_enemy(self, new_position):
        '''
        Function is used to move enemy around the map.
        :param new_position: the new position of enemy;
        :return: a cell on which enemy will stay after moving;
        :type new_position: tuple: (int, int);
        :rtype: DungeonCell
        '''
        old_x, old_y = self.__enemy_position
        self.__enemy_position = new_position
        new_x, new_y = self.__enemy_position
        previous_cell = self.dungeon_map[new_x][new_y]
        self.dungeon_map[old_x][old_y] = DungeonCell.EMPTY
        self.dungeon_map[new_x][new_y] = DungeonCell.ENEMY
        return previous_cell


    @logger_decorator
    def get_cell_on_position(self, position):
        '''
        Function returns a dundeon cell on position;
        :param position: a position on map;
        :return: a cell on map;
        :type position: tuple: (int, int);
        :rtype: DungeonCell.
        '''
        x, y = position
        return self.dungeon_map[x][y]


    @logger_decorator
    def add_enemy_on_position(self, position):
        '''
        Method is used to add an enemy on position. In current implementation the game can only have 1 enemy.
        :param position: a position of added enemy;
        :type position: tuple: (int, int).
        '''
        self.__enemy_position = position
        x, y = self.__enemy_position
        self.dungeon_map[x][y] = DungeonCell.ENEMY


    @logger_decorator
    def output(self, dungeon_cell_to_output_symbol):
        '''
        Function is used to output a map for Dungeon Game.
        :param dungeon_map: a map to output;
        :param dungeon_cell_to_output_symbol: a map that will be used to output the cells
        :type dungeon_map: a list of lists of DungeonCells; 
        :type dungeon_cell_to_output_symbol: a dict with key type: DungeonCell, value type: str.
        '''
        # i guess there must be more efficient way to format such string
        lock_string = ''.join('-' * len(self.dungeon_map))

        logging.info(lock_string)

        row_to_string = lambda row: ''.join(dungeon_cell_to_output_symbol[x] for x in row)
        map_string = '\n'.join(row_to_string(row) for row in self.dungeon_map)
        logging.info(map_string)

        logging.info(lock_string)

    
    @logger_decorator
    def get_cells_near(self, position):
        '''
        Function used to get all cells that are near the position on map;
        :param position: a position on map;
        :param dungeon_map: a map used for dungeon game;
        :return: all cells near position;
        :type position: a tuple of 2 ints;
        :rtype: a list of DungeonCells.
        '''
        map_size = len(self.dungeon_map)
        x, y = position

        cells = []
        if x != 0:
            cells.append(self.dungeon_map[x - 1][y])
        
        if x != map_size - 1:
            cells.append(self.dungeon_map[x + 1][y])

        if y != 0:
            cells.append(self.dungeon_map[x][y - 1])

        if y != map_size - 1:
            cells.append(self.dungeon_map[x][y + 1])

        assert(len(cells) >= 2 and len(cells) <= 4)

        return cells

    
    @logger_decorator
    def get_positions_near(self, position):
        '''
        Method is used to get positions near given position on the map.
        :param position: a position;
        :return: positions near the position;
        :type position: tuple: (int, int);
        :rtype: a list of tuples (int, int).
        '''
        x, y = position
        near_positions = []
        if x != 0:
            near_positions.append((x - 1, y))
        
        if x != self.__size - 1:
            near_positions.append((x + 1, y))

        if y != 0:
            near_positions.append((x, y - 1))

        if y != self.__size - 1:
            near_positions.append((x, y + 1))

        return near_positions


    @logger_decorator
    def get_random_cell_if(self, condition):
        '''
        Method is used to get a random cell on map if some conditional function returns True.
        :param condition: a function that expects a parameter of type DungeonCell and retunts bool;
        :type condition: any callable type.
        '''
        filtered_cells = []
        for i in range(self.__size):
            for j in range(self.__size):
                if condition(self.dungeon_map[i][j]):
                    filtered_cells.append((i, j))
        return random.choice(filtered_cells)


    @logger_decorator
    def update(self):
        super().update()

        self.output(self.__hide_everything_except_player_map)

        cells_near_player = self.get_cells_near(self.__player_position)

        traps_nearby = [cell for cell in cells_near_player if cell is DungeonCell.TRAP]
        if traps_nearby:
            logging.info(f'Warning! There is {len(traps_nearby)} traps nearby!')
        
        treasures_nearby = [cell for cell in cells_near_player if cell is DungeonCell.TREASURE]
        if treasures_nearby:
            logging.info(f'Wow! There is {len(treasures_nearby)} treasures just near you! Good luck!')
