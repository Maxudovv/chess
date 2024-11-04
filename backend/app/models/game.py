import io
import uuid

import chess.pgn
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from stockfish import Stockfish


class Game(models.Model):
    class Status(models.TextChoices):
        pending = "pending", "Ожидание"
        in_progress = "in_progress", "В процессе"
        finished = "finished", "Завершено"

    class Colour(models.TextChoices):
        white = "white", "Белый"
        black = "black", "Черный"

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    started_at = models.DateTimeField(null=True)
    player = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True)
    colour = models.CharField(max_length=10, choices=Colour.choices)
    finished_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.pending)
    pgn = models.TextField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Games"

    def get_game(self) -> chess.pgn.Game:
        pgn_io = io.StringIO(self.pgn)
        print(f"{pgn_io.getvalue()=}")
        return chess.pgn.read_game(pgn_io)

    def get_board(self) -> chess.Board:
        game = self.get_game()
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
        return board

    def make_move(self, move_uci: str, source: "Move.Source"):
        board = self.get_board()
        board.push_uci(move_uci)
        print(f"{board.fen()=}")
        print(f"{move_uci=}")
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

    def make_bot_move(self):
        stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
        print("nigga", self.get_board().fen())
        stockfish.set_fen_position(self.get_board().fen())
        move_uci = stockfish.get_best_move()
        self.make_move(move_uci=move_uci, source=Move.Source.bot)
        return move_uci


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
