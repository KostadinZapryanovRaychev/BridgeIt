from typing import Tuple, Optional
import re

def parse_move_input(input_str: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Parse user input for a move.
    Expected formats:
    - "0,0 0,1" (connect node (0,0) to node (0,1))
    - "(0,0)-(0,1)" 
    - "0 0 to 0 1"
    """
    input_str = input_str.strip().lower()
    
    # Pattern 1: "0,0 0,1" or "0,0-0,1"
    pattern1 = r'(\d+),(\d+)[\s\-]+(\d+),(\d+)'
    match = re.match(pattern1, input_str)
    if match:
        r1, c1, r2, c2 = map(int, match.groups())
        return ((r1, c1), (r2, c2))
    
    # Pattern 2: "0 0 to 0 1" or "0 0 0 1"
    pattern2 = r'(\d+)\s+(\d+)(?:\s+to\s+|\s+)(\d+)\s+(\d+)'
    match = re.match(pattern2, input_str)
    if match:
        r1, c1, r2, c2 = map(int, match.groups())
        return ((r1, c1), (r2, c2))
    
    return None

def are_adjacent_nodes(node1: Tuple[int, int], node2: Tuple[int, int]) -> bool:
    """Check if two nodes are adjacent (horizontally or vertically)."""
    r1, c1 = node1
    r2, c2 = node2
    
    # Same row, adjacent columns
    if r1 == r2 and abs(c1 - c2) == 1:
        return True
    
    # Same column, adjacent rows
    if c1 == c2 and abs(r1 - r2) == 1:
        return True
    
    return False

def format_move(node1: Tuple[int, int], node2: Tuple[int, int]) -> str:
    """Format a move for display."""
    return f"({node1[0]},{node1[1]}) → ({node2[0]},{node2[1]})"

def get_move_description(node1: Tuple[int, int], node2: Tuple[int, int]) -> str:
    """Get a human-readable description of a move."""
    r1, c1 = node1
    r2, c2 = node2
    
    if r1 == r2:  # Horizontal move
        direction = "right" if c2 > c1 else "left"
        return f"Horizontal bridge from ({r1},{c1}) going {direction}"
    else:  # Vertical move
        direction = "down" if r2 > r1 else "up"
        return f"Vertical bridge from ({r1},{c1}) going {direction}"

def validate_board_size(rows: int, cols: int) -> bool:
    """Validate board size parameters."""
    return 3 <= rows <= 20 and 3 <= cols <= 20

def print_help():
    """Print help information for the game."""
    help_text = """
Bridge It Game Help
==================

OBJECTIVE:
- Player 1 (Red ═══): Connect the top and bottom edges of the board
- Player 2 (Blue ───): Connect the left and right edges of the board

HOW TO PLAY:
1. Players take turns placing bridges between adjacent nodes
2. Enter your move by specifying two adjacent nodes
3. First player to create a continuous path wins!

MOVE INPUT FORMATS:
- "0,0 0,1"     - Connect node (0,0) to node (0,1)
- "0 0 to 0 1"  - Same as above, different format
- "2,1-2,2"     - Connect node (2,1) to node (2,2)

COMMANDS:
- "help" or "h"     - Show this help
- "quit" or "q"     - Quit the game
- "undo" or "u"     - Undo last move
- "reset" or "r"    - Reset the game
- "info" or "i"     - Show game information

BOARD SYMBOLS:
- ●           - Node (intersection point)
- ═══         - Player 1's bridge (Red)
- ───         - Player 2's bridge (Blue)
- (empty)     - Available bridge position

COORDINATES:
- Nodes are numbered starting from (0,0) at top-left
- Row numbers increase going down
- Column numbers increase going right
"""
    print(help_text)