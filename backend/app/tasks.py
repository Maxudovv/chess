from celery import shared_task
import chess.engine
import os

from django.conf import settings

from rabbit import Rabbit


@shared_task
def make_bot_move(game_id: str):
    from app.models import Game
    from app.models.game import Move

    game = Game.objects.get(id=game_id)
    with chess.engine.SimpleEngine.popen_uci(settings.STOCKFISH_PATH) as engine:
        board = chess.Board(fen=game.get_board().fen())
        result = engine.play(board, chess.engine.Limit(time=1.0))
        move_uci = result.move.uci()
    game.make_move(move_uci=move_uci, source=Move.Source.bot)

    rabbitmq = Rabbit()
    rabbitmq.send_move(game_id, move_uci=move_uci)
