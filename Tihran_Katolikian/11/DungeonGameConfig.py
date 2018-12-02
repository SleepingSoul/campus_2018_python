import json
import logging
from sys import exit


config_filename = 'dungeon_game_config.json'

IS_DEBUG_MODE = None
PLAYER_HP = None
NUMBER_OF_TREASURES_TO_WIN = None
ENEMY_DAMAGE = None
ENEMY_SPEED = None

def load_config():
    '''
    The function is used to load config variables from a JSON file. This function will be executed only once when file
    will be firstly imported.
    '''
    try:
        with open(config_filename, 'r') as config_file:
            config_variables = json.load(config_file)
            # is there some way to not write string rep of this variable?
            global IS_DEBUG_MODE
            global PLAYER_HP
            global NUMBER_OF_TREASURES_TO_WIN
            global ENEMY_DAMAGE
            global ENEMY_SPEED	

            IS_DEBUG_MODE = config_variables['IS_DEBUG_MODE']
            PLAYER_HP = config_variables['PLAYER_HP']
            NUMBER_OF_TREASURES_TO_WIN = config_variables['NUMBER_OF_TREASURES_TO_WIN']
            ENEMY_DAMAGE = config_variables['ENEMY_DAMAGE']
            ENEMY_SPEED = config_variables['ENEMY_SPEED']
    except FileNotFoundError as error:
        logging.critical("Config file not found: program cannot be executed properly without config.")
        exit(f'No config file found on address: {config_filename}')


load_config()
