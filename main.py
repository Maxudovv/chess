from stockfish import Stockfish

stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")

stockfish.make_moves_from_current_position(["e2e4", "e7e5"])
print(stockfish.get_evaluation())
print(stockfish.get_board_visual())

