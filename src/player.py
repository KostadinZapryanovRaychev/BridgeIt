from enum import Enum

class PlayerType(Enum):
    HUMAN = "human"
    AI = "ai"

class Player:
    """Represents a player in the Bridge It game."""
    
    def __init__(self, player_id: int, name: str, color: str, player_type: PlayerType = PlayerType.HUMAN):
        self.player_id = player_id  # 1 or 2
        self.name = name
        self.color = color
        self.player_type = player_type
        self.moves_made = 0
    
    def __str__(self) -> str:
        return f"Player {self.player_id} ({self.name}) - {self.color}"
    
    def __repr__(self) -> str:
        return f"Player(id={self.player_id}, name='{self.name}', color='{self.color}')"