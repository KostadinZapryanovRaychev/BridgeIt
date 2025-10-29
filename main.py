#!/usr/bin/env python3
"""
Bridge It Game - Main Entry Point
A console-based implementation of the Bridge It connection game.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import BridgeItGame, PlayerType, parse_move_input, are_adjacent_nodes, format_move, print_help, validate_board_size

def get_game_settings():
    """Get game settings from user."""
    print("🌉 Welcome to Bridge It Game! 🌉")
    print("=" * 40)
    
    # Get board size
    while True:
        try:
            size_input = input("Enter board size (rows cols) [default: 6 6]: ").strip()
            if not size_input:
                rows, cols = 6, 6
                break
            
            parts = size_input.split()
            if len(parts) != 2:
                print("Please enter two numbers for rows and columns.")
                continue
            
            rows, cols = int(parts[0]), int(parts[1])
            if not validate_board_size(rows, cols):
                print("Board size must be between 3x3 and 20x20.")
                continue
            
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    # Get player names
    player1_name = input("Enter Player 1 name [Red player - connects top↔bottom]: ").strip()
    if not player1_name:
        player1_name = "Player 1"
    
    player2_name = input("Enter Player 2 name [Blue player - connects left↔right]: ").strip()
    if not player2_name:
        player2_name = "Player 2"
    
    return rows, cols, player1_name, player2_name

def handle_game_command(command: str, game: BridgeItGame) -> bool:
    """Handle special game commands. Returns True if game should continue."""
    command = command.lower().strip()
    
    if command in ['quit', 'q', 'exit']:
        print("Thanks for playing Bridge It! 👋")
        return False
    
    elif command in ['help', 'h']:
        print_help()
        return True
    
    elif command in ['info', 'i']:
        info = game.get_game_info()
        print("\n📊 Game Information:")
        print(f"State: {info['state']}")
        print(f"Moves made: {info['moves_made']}")
        print(f"Board size: {info['board_size']}")
        for player_info in info['players']:
            print(f"  {player_info['name']}: {player_info['moves']} moves - {player_info['goal']}")
        print()
        return True
    
    elif command in ['undo', 'u']:
        if game.undo_last_move():
            print("✅ Last move undone.")
        else:
            print("❌ No moves to undo.")
        return True
    
    elif command in ['reset', 'r']:
        confirm = input("Are you sure you want to reset the game? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            game.reset_game()
            if len(game.players) == 2:
                game.start_game()
            print("🔄 Game reset!")
        return True
    
    else:
        print(f"Unknown command: {command}")
        print("Type 'help' for available commands.")
        return True

def play_game():
    """Main game loop."""
    # Get game settings
    rows, cols, player1_name, player2_name = get_game_settings()
    
    # Create game
    game = BridgeItGame(rows, cols)
    game.add_player(player1_name, "Red", PlayerType.HUMAN)
    game.add_player(player2_name, "Blue", PlayerType.HUMAN)
    game.start_game()
    
    print(f"\n🎮 Starting {rows}x{cols} Bridge It Game!")
    print(f"Players: {player1_name} (Red ═══) vs {player2_name} (Blue ───)")
    print("\nType 'help' for commands and rules.")
    print("=" * 50)
    
    # Main game loop
    while game.game_state == "playing":
        # Display current state
        print("\n" + game.display_board())
        
        current_player = game.get_current_player()
        print(f"\n{current_player.name}'s turn ({current_player.color})")
        
        # Get user input
        user_input = input("Enter your move (or command): ").strip()
        
        if not user_input:
            continue
        
        # Check if it's a command
        if user_input.lower() in ['quit', 'q', 'exit', 'help', 'h', 'info', 'i', 'undo', 'u', 'reset', 'r']:
            if not handle_game_command(user_input, game):
                break
            continue
        
        # Try to parse as a move
        move = parse_move_input(user_input)
        if not move:
            print("❌ Invalid move format. Type 'help' for examples.")
            continue
        
        node1, node2 = move
        
        # Validate the move
        if not are_adjacent_nodes(node1, node2):
            print("❌ Nodes must be adjacent (horizontally or vertically).")
            continue
        
        # Check if nodes are within board bounds
        if (not (0 <= node1[0] < rows and 0 <= node1[1] < cols) or 
            not (0 <= node2[0] < rows and 0 <= node2[1] < cols)):
            print(f"❌ Nodes must be within board bounds (0-{rows-1}, 0-{cols-1}).")
            continue
        
        # Try to make the move
        if game.make_move(node1, node2):
            print(f"✅ {current_player.name} placed bridge: {format_move(node1, node2)}")
            
            # Check if game ended
            if game.winner:
                print("\n" + game.display_board())
                print(f"\n🎉 GAME OVER! 🎉")
                print(f"Winner: {game.winner.name} ({game.winner.color})")
                print(f"Total moves: {len(game.move_history)}")
                break
        else:
            print("❌ Invalid move. That position is already occupied.")
    
    # Ask if player wants to play again
    print("\n" + "=" * 50)
    play_again = input("Would you like to play again? (y/N): ").strip().lower()
    if play_again in ['y', 'yes']:
        play_game()

def main():
    """Main entry point."""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing! 👋")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please report this issue if it persists.")

if __name__ == "__main__":
    main()