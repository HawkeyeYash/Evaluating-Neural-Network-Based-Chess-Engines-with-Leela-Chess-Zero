import chess.pgn
import os

# Analyze game statistics from a single PGN file
def analyze_game_statistics(file_path):
    # Initialize statistics
    stats = {
        "total_games": 0,
        "avg_moves": 0,
        "white_wins": 0,
        "black_wins": 0,
        "draws": 0,
    }

    # Initialize total moves counter
    total_moves = 0

    # Open the PGN file to read games
    with open(file_path, "r") as f:
        while True:
            # Read each game using python-chess
            game = chess.pgn.read_game(f)

            # Check if the game is valid
            if game is None:
                break

            # Increment game count
            stats["total_games"] += 1

            # Count moves in the game
            move_count = 0
            node = game
            while node.variations:
                node = node.variations[0]
                move_count += 1
            total_moves += move_count

            # Analyze the result of the game
            result = game.headers.get("Result", "")
            if result == "1-0":
                stats["white_wins"] += 1
            elif result == "0-1":
                stats["black_wins"] += 1
            elif result == "1/2-1/2":
                stats["draws"] += 1

    # Calculate average moves per game
    if stats["total_games"] > 0:
        stats["avg_moves"] = total_moves / stats["total_games"]

    return stats

# Combine statistics from multiple files
def combine_statistics(stats_list):
    combined_stats = {
        "total_games": 0,
        "avg_moves": 0,
        "white_wins": 0,
        "black_wins": 0,
        "draws": 0,
    }

    total_moves = 0

    for stats in stats_list:
        combined_stats["total_games"] += stats["total_games"]
        combined_stats["white_wins"] += stats["white_wins"]
        combined_stats["black_wins"] += stats["black_wins"]
        combined_stats["draws"] += stats["draws"]
        total_moves += stats["avg_moves"] * stats["total_games"]

    if combined_stats["total_games"] > 0:
        combined_stats["avg_moves"] = total_moves / combined_stats["total_games"]

    return combined_stats

# Main function
def main():
    # Directory containing the PGN files
    input_directory = "leela-chess-zero-self-play-chess-games-bundle"

    # List to store statistics for each file
    all_stats = []

    # Iterate through all files in the directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".pgn"):
            file_path = os.path.join(input_directory, file_name)
            print(f"Processing file: {file_name}")

            # Analyze statistics for the current file
            stats = analyze_game_statistics(file_path)
            all_stats.append(stats)

    # Combine statistics from all files
    combined_stats = combine_statistics(all_stats)

    # Print combined statistics
    print(f"Combined Game Statistics:\n{combined_stats}")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()