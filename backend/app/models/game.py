import io
import logging
import uuid

import chess.pgn
from chess import Termination
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from stockfish import Stockfish

from app.exceptions import GameOverException
from app.tasks import make_bot_move, perform_resignation_task, notify_game_is_over
from config.utils import is_celery_alive


class Game(models.Model):
    class Status(models.TextChoices):
        pending = "pending", "Ожидание"
        in_progress = "in_progress", "В процессе"
        finished = "finished", "Завершено"

    class Colour(models.TextChoices):
        white = "white", "Белый"
        black = "black", "Черный"

    class FinishReason(models.TextChoices):
        checkmate = "checkmate", "Мат"
        stalemate = "stalemate", "Пат"
        resignation = "resignation", "Сдача"
        insufficient_material = "insufficient_material", "Недостаточно материала"
        threefold_repetition = "threefold_repetition", "Троекратное повторение"
        fifty_move_rule = "fifty_move_rule", "Правило 50 ходов"

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    started_at = models.DateTimeField(null=True)
    player = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True)
    colour = models.CharField(max_length=10, choices=Colour.choices)
    finished_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.pending)
    finish_reason = models.CharField(max_length=50, choices=FinishReason.choices, null=True)
    winner_colour = models.CharField(max_length=10, choices=Colour.choices, null=True)

    pgn = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Games"

    def get_game(self) -> chess.pgn.Game:
        pgn_io = io.StringIO(self.pgn)
        return chess.pgn.read_game(pgn_io)

    def get_board(self) -> chess.Board:
        game = self.get_game()
        board = game.board()
        board.is_game_over()
        for move in game.mainline_moves():
            board.push(move)
        return board

    def make_move(self, move_uci: str, source: "Move.Source"):
        board = self.get_board()
        board.push_uci(move_uci)
        Move.objects.create(
            game=self,
            number=len(board.move_stack),
            text=move_uci,
            fen=board.fen(),
            source=source
        )

        game = chess.pgn.Game.from_board(board)
        self.pgn = str(game)
        self.save(update_fields=["pgn"])

    def perform_stockfish_move(self):
        board = self.get_board()
        if board.is_game_over(claim_draw=True):
            raise GameOverException()
        if is_celery_alive():
            make_bot_move.delay(str(self.id))
        else:
            make_bot_move(str(self.id))

    def perform_game_finish(self):
        board = self.get_board()
        outcome = board.outcome(claim_draw=True)
        if outcome is None:
            raise Exception("Game is not over")

        reasons = {
            Termination.CHECKMATE: Game.FinishReason.checkmate,
            Termination.STALEMATE: Game.FinishReason.stalemate,
            Termination.INSUFFICIENT_MATERIAL: Game.FinishReason.insufficient_material,
            Termination.FIFTY_MOVES: Game.FinishReason.fifty_move_rule,
            Termination.THREEFOLD_REPETITION: Game.FinishReason.threefold_repetition,
        }
        try:
            reason = reasons[outcome.termination]
        except KeyError:
            logging.error(f"Unknown termination '{outcome.termination}'")
            return
        self.finish_reason = reason
        self.finished_at = timezone.now()
        self.winner_colour = (Game.Colour.white if outcome.winner else Game.Colour.black) if outcome.winner is not None else None
        self.status = Game.Status.finished
        self.save(update_fields=["finish_reason", "finished_at", "winner_colour", "status"])

        # Notify rabbitmq
        if is_celery_alive():
            notify_game_is_over.delay(str(self.id))
        else:
            notify_game_is_over(str(self.id))

    def perform_resignation(self):
        if is_celery_alive():
            perform_resignation_task.delay(str(self.id))
        else:
            perform_resignation_task(str(self.id))


class Move(models.Model):
    class Source(models.TextChoices):
        user = "user", "Пользователь"
        bot = "bot", "Бот"

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False,
                          primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.CharField(max_length=10)
    fen = models.TextField()
    source = models.CharField(max_length=10, choices=Source.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('game_id', 'number'),)
