# from stockfish import Stockfish
#
# stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
#
# # stockfish.make_moves_from_current_position(["e2e4", "e7e5"])
# stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq - 0 1")
# print(stockfish.get_board_visual())
# stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
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
import chess

b = chess.Board(fen="rn1qkbnr/ppp2ppp/4p3/3p4/3P4/5P2/PPP2P1P/RNBQKB1R w KQkq - 0 5")
print(b)
