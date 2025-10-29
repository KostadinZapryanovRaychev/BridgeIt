from typing import List, Tuple, Optional
from .board import Board
from .player import Player, PlayerType

class GameState:
    """Represents the current state of the game."""
    SETUP = "setup"
    PLAYING = "playing"
    FINISHED = "finished"

class BridgeItGame:
    """Main game class that manages the Bridge It game."""
    
    def __init__(self, board_rows: int = 6, board_cols: int = 6):
        self.board = Board(board_rows, board_cols)
        self.players: List[Player] = []
        self.current_player_index = 0
        self.game_state = GameState.SETUP
        self.winner: Optional[Player] = None
        self.move_history: List[Tuple[Tuple[int, int], Tuple[int, int], int]] = []
    
    def add_player(self, name: str, color: str, player_type: PlayerType = PlayerType.HUMAN) -> Player:
        """Add a player to the game."""
        if len(self.players) >= 2:
            raise ValueError("Game already has 2 players")
        
        player_id = len(self.players) + 1
        player = Player(player_id, name, color, player_type)
        self.players.append(player)
        return player
    
    def start_game(self) -> bool:
        """Start the game if both players are ready."""
        if len(self.players) != 2:
            return False
        
        self.game_state = GameState.PLAYING
        self.current_player_index = 0  # Player 1 goes first
        return True
    
    def get_current_player(self) -> Optional[Player]:
        """Get the current player."""
        if self.game_state != GameState.PLAYING or not self.players:
            return None
        return self.players[self.current_player_index]
    
    def make_move(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> bool:
        """
        Make a move for the current player.
        Returns True if the move was successful, False otherwise.
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        current_player = self.get_current_player()
        if not current_player:
            return False
        
        # Try to place the bridge
        if self.board.place_bridge(node1, node2, current_player.player_id):
            # Record the move
            self.move_history.append((node1, node2, current_player.player_id))
            current_player.moves_made += 1
            
            # Check for win condition
            if self.board.has_winning_path(current_player.player_id):
                self.winner = current_player
                self.game_state = GameState.FINISHED
                return True
            
            # Switch to next player
            self.current_player_index = 1 - self.current_player_index
            return True
        
        return False
    
    def is_valid_move(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> bool:
        """Check if a move is valid."""
        return self.board.is_valid_move(node1, node2)
    
    def get_available_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all available moves (empty edges)."""
        moves = []
        for edge, state in self.board.edges.items():
            if state.value == 0:  # EdgeState.EMPTY
                moves.append(edge)
        return moves
    
    def undo_last_move(self) -> bool:
        """Undo the last move (if any)."""
        if not self.move_history or self.game_state == GameState.FINISHED:
            return False
        
        # Get the last move
        node1, node2, player_id = self.move_history.pop()
        
        # Remove the bridge from the board
        edge = self.board._normalize_edge(node1, node2)
        self.board.edges[edge] = self.board.edges[edge].__class__(0)  # EdgeState.EMPTY
        
        # Update player stats
        for player in self.players:
            if player.player_id == player_id:
                player.moves_made -= 1
                break
        
        # Switch back to previous player
        self.current_player_index = 1 - self.current_player_index
        
        return True
    
    def get_game_info(self) -> dict:
        """Get current game information."""
        current_player = self.get_current_player()
        return {
            'state': self.game_state,
            'current_player': current_player.name if current_player else None,
            'current_player_id': current_player.player_id if current_player else None,
            'winner': self.winner.name if self.winner else None,
            'moves_made': len(self.move_history),
            'board_size': f"{self.board.rows}x{self.board.cols}",
            'players': [
                {
                    'name': p.name,
                    'color': p.color,
                    'moves': p.moves_made,
                    'goal': 'Connect Top-Bottom' if p.player_id == 1 else 'Connect Left-Right'
                } for p in self.players
            ]
        }
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = Board(self.board.rows, self.board.cols)
        self.current_player_index = 0
        self.game_state = GameState.SETUP if len(self.players) != 2 else GameState.PLAYING
        self.winner = None
        self.move_history = []
        for player in self.players:
            player.moves_made = 0
    
    def display_board(self) -> str:
        """Display the current board state."""
        board_display = self.board.display()
        
        # Add game info
        info_lines = []
        info_lines.append(f"Bridge It Game - {self.board.rows}x{self.board.cols} Board")
        info_lines.append("=" * 40)
        
        for player in self.players:
            goal = "Top↔Bottom" if player.player_id == 1 else "Left↔Right"
            symbol = "═══" if player.player_id == 1 else "───"
            marker = "→" if self.get_current_player() == player else " "
            info_lines.append(f"{marker} {player.name} ({player.color}) {symbol} Goal: {goal}")
        
        info_lines.append("")
        
        if self.winner:
            info_lines.append(f"🎉 Winner: {self.winner.name} ({self.winner.color})!")
        elif self.game_state == GameState.PLAYING:
            current = self.get_current_player()
            info_lines.append(f"Current turn: {current.name} ({current.color})")
        
        info_lines.append("")
        
        return "\n".join(info_lines) + "\n" + board_display