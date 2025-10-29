from typing import List, Tuple, Set, Optional
from enum import Enum

class EdgeState(Enum):
    EMPTY = 0
    PLAYER1 = 1  # Red player
    PLAYER2 = 2  # Blue player

class Board:
    """
    Represents the Bridge It game board.
    The board consists of nodes (dots) arranged in a grid,
    with edges (potential bridge positions) between adjacent nodes.
    """
    
    def __init__(self, rows: int = 6, cols: int = 6):
        self.rows = rows
        self.cols = cols
        
        # Dictionary to store edge states
        # Key: (node1, node2) where node1 < node2
        # Value: EdgeState
        self.edges = {}
        
        # Initialize all possible edges
        self._initialize_edges()
    
    def _initialize_edges(self):
        """Initialize all possible edges between adjacent nodes."""
        for row in range(self.rows):
            for col in range(self.cols):
                # Horizontal edges (to the right neighbor)
                if col < self.cols - 1:
                    edge = self._normalize_edge((row, col), (row, col + 1))
                    self.edges[edge] = EdgeState.EMPTY
                
                # Vertical edges (to the bottom neighbor)
                if row < self.rows - 1:
                    edge = self._normalize_edge((row, col), (row + 1, col))
                    self.edges[edge] = EdgeState.EMPTY
    
    def _normalize_edge(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Normalize edge representation to ensure consistent ordering."""
        return (node1, node2) if node1 < node2 else (node2, node1)
    
    def is_valid_move(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> bool:
        """Check if placing a bridge between two nodes is valid."""
        edge = self._normalize_edge(node1, node2)
        return edge in self.edges and self.edges[edge] == EdgeState.EMPTY
    
    def place_bridge(self, node1: Tuple[int, int], node2: Tuple[int, int], player: int) -> bool:
        """
        Place a bridge between two nodes for the given player.
        Returns True if successful, False otherwise.
        """
        if not self.is_valid_move(node1, node2):
            return False
        
        edge = self._normalize_edge(node1, node2)
        player_state = EdgeState.PLAYER1 if player == 1 else EdgeState.PLAYER2
        self.edges[edge] = player_state
        return True
    
    def get_edge_state(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> EdgeState:
        """Get the state of an edge between two nodes."""
        edge = self._normalize_edge(node1, node2)
        return self.edges.get(edge, EdgeState.EMPTY)
    
    def get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get all valid neighboring nodes for a given node."""
        row, col = node
        neighbors = []
        
        # Check all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def get_player_edges(self, player: int) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all edges belonging to a specific player."""
        player_state = EdgeState.PLAYER1 if player == 1 else EdgeState.PLAYER2
        return {edge for edge, state in self.edges.items() if state == player_state}
    
    def has_winning_path(self, player: int) -> bool:
        """
        Check if a player has a winning path.
        Player 1 (Red) wins by connecting top and bottom.
        Player 2 (Blue) wins by connecting left and right.
        """
        if player == 1:
            # Check if there's a path from top row to bottom row
            start_nodes = [(0, col) for col in range(self.cols)]
            end_nodes = [(self.rows - 1, col) for col in range(self.cols)]
        else:
            # Check if there's a path from left column to right column
            start_nodes = [(row, 0) for row in range(self.rows)]
            end_nodes = [(row, self.cols - 1) for row in range(self.rows)]
        
        return self._has_path_between_sets(start_nodes, end_nodes, player)
    
    def _has_path_between_sets(self, start_nodes: List[Tuple[int, int]], 
                              end_nodes: List[Tuple[int, int]], player: int) -> bool:
        """Check if there's a path between any start node and any end node."""
        visited = set()
        
        def dfs(node: Tuple[int, int]) -> bool:
            if node in visited:
                return False
            if node in end_nodes:
                return True
            
            visited.add(node)
            
            # Check all neighbors connected by player's bridges
            for neighbor in self.get_neighbors(node):
                edge_state = self.get_edge_state(node, neighbor)
                player_state = EdgeState.PLAYER1 if player == 1 else EdgeState.PLAYER2
                
                if edge_state == player_state:
                    if dfs(neighbor):
                        return True
            
            return False
        
        # Try starting from each start node
        for start_node in start_nodes:
            visited.clear()
            if dfs(start_node):
                return True
        
        return False
    
    def display(self) -> str:
        """Return a string representation of the board."""
        result = []
        
        for row in range(self.rows):
            # Display nodes and horizontal edges
            line = ""
            for col in range(self.cols):
                line += "●"  # Node
                
                if col < self.cols - 1:  # Horizontal edge
                    edge_state = self.get_edge_state((row, col), (row, col + 1))
                    if edge_state == EdgeState.PLAYER1:
                        line += "═══"
                    elif edge_state == EdgeState.PLAYER2:
                        line += "───"
                    else:
                        line += "   "
            
            result.append(line)
            
            # Display vertical edges (except for last row)
            if row < self.rows - 1:
                line = ""
                for col in range(self.cols):
                    edge_state = self.get_edge_state((row, col), (row + 1, col))
                    if edge_state == EdgeState.PLAYER1:
                        line += "║"
                    elif edge_state == EdgeState.PLAYER2:
                        line += "|"
                    else:
                        line += " "
                    
                    if col < self.cols - 1:
                        line += "   "
                
                result.append(line)
        
        return "\n".join(result)