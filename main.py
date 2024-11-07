from stockfish import Stockfish
import chess.pgn

stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")

# stockfish.make_moves_from_current_position(["e2e4", "e7e5"])
board = chess.Board()
board.push_uci("e2e4")
board.push_uci("e7e5")
board.push_uci("d1h5")
board.push_uci("b8c6")
board.push_uci("f1c4")
board.push_uci("g8f6")
board.push_uci("h5f7")
b = chess.pgn.Game.from_board(board)
print(board)
print(b)
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# print(stockfish.get_board_visual())
# # print(stockfish.get_evaluation())
# # print(stockfish.get_board_visual())
# #
# # stockfish
# # import io
# #
# # import chess.pgn
# #
# # pgn_string = """
# # [Site "Example Site"]
# # """
# #
# # pgn_io = io.StringIO(pgn_string)
# # game = chess.pgn.read_game(pgn_io)
# # board = game.board()
# # # print(board.fen())
# # # print(board.is_game_over())
# # # print(board.is_checkmate())
# # print(board.push_uci("g1f3"))
# # print(board.push_uci("b8c6"))
# # print(board.move_stack)
# # print(board.fullmove_number)
# import chess
#
# board = chess.Board()
# board.push_uci("g2g4")
# board.push_uci("d7d5")
# board.push_uci("g1f3")
# print(board)
# print(board.move_stack)
#
import chess.engine
from stockfish import Stockfish

# b = chess.Board()
# stockfish = Stockfish("/opt/homebrew/bin/stockfish")
# stockfish.set_fen_position(b.fen())
# print(stockfish.get_best_move())
# with chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish") as engine:
#     result = engine.play(b, chess.engine.Limit(time=1.0))
#     print("Nigga", result.move.uci())



"docker run -d --name rabbit rabbitmq:latest"
