import chess.pgn
import pandas as pd
from tqdm import tqdm

def parse_pgn_to_csv(pgn_file, output_csv):
    games_data = []

    # Initialize progress bar with dynamic updates
    with open(pgn_file) as pgn, tqdm(desc="Processing Games", unit="games") as pbar:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            # Extract metadata
            headers = game.headers
            event = headers.get("Event", "Unknown")
            site = headers.get("Site", "Unknown")
            date = headers.get("Date", "Unknown")
            round = headers.get("Round", "Unknown")
            white_player = headers.get("White", "Unknown")
            black_player = headers.get("Black", "Unknown")
            result = headers.get("Result", "Unknown")
            eco = headers.get("ECO", "Unknown")
            game_duration = headers.get("GameDuration", "Unknown")
            game_end_time = headers.get("GameEndTime", "Unknown")
            game_start_time = headers.get("GameStartTime", "Unknown")
            opening = headers.get("Opening", "Unknown")
            playcount = headers.get("PlyCount", "Unknown")
            timecontrol = headers.get("TimeControl", "Unknown")
            variation = headers.get("Variation", "Unknown")

            # Extract moves as a single string
            moves = []
            node = game
            while node.variations:
                next_node = node.variation(0)
                moves.append(node.board().san(next_node.move))
                node = next_node
            moves_str = " ".join(moves)

            # Append the game data to the list
            games_data.append({
                "Event": event,
                "Site": site,
                "Date": date,
                "Round": round,
                "White": white_player,
                "Black": black_player,
                "Result": result,
                "ECO": eco,
                "GameDuration": game_duration,
                "GameEndTime": game_end_time,
                "GameStartTime": game_start_time,
                "Opening": opening,
                "PlyCount": playcount,
                "TimeControl": timecontrol,
                "Variation": variation,
                "Moves": moves_str
            })

            # Update progress bar dynamically
            pbar.update(1)

    # Save to CSV
    df = pd.DataFrame(games_data)
    df.to_csv(output_csv, index=False)
    print(f"Saved to {output_csv}")