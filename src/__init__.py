"""
Bridge It Game Package
A Python implementation of the Bridge It connection game.
"""

from .board import Board, EdgeState
from .player import Player, PlayerType
from .game import BridgeItGame, GameState
from .utils import parse_move_input, are_adjacent_nodes, format_move, print_help, validate_board_size

__version__ = "1.0.0"
__author__ = "Bridge It Game Developer"

__all__ = [
    'Board', 'EdgeState',
    'Player', 'PlayerType', 
    'BridgeItGame', 'GameState',
    'parse_move_input', 'are_adjacent_nodes', 'format_move', 'print_help', 'validate_board_size'
]