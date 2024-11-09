from celery import shared_task
import chess.engine

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

    board = game.get_board()
    if board.is_game_over(claim_draw=True):
        game.perform_game_finish()


@shared_task
def perform_resignation_task(game_id: str):
    from app.models import Game

    game = Game.objects.get(id=game_id)
    game.status = Game.Status.finished
    game.finish_reason = Game.FinishReason.resignation
    game.winner_colour = "black" if game.colour == "white" else "white"
    game.save(update_fields=["status", "finish_reason", "winner_colour"])

    rabbitmq = Rabbit()
    rabbitmq.send_game_finished(
        game_id=game_id,
        reason=Game.FinishReason.resignation,
        winner_colour=game.winner_colour
    )


@shared_task
def notify_game_is_over(game_id: str):
    from app.models import Game

    game = Game.objects.get(id=game_id)
    rabbitmq = Rabbit()
    rabbitmq.send_game_finished(
        game_id=game_id,
        reason=game.finish_reason,
        winner_colour=game.winner_colour
    )
