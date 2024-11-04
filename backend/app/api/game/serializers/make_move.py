import io

import chess.pgn
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models.game import Move, Game


class MakeMoveSerializer(serializers.ModelSerializer):
    output_move = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Move
        fields = (
            "game",
            "text",
            "output_move",
        )

    def get_output_move(self, data: dict):
        game = data["game"]
        board = game.get_board()
        last_move = board.move_stack[-1]
        return last_move.uci()

    def validate(self, attrs):
        data = super().validate(attrs)
        game = data["game"]
        user = self.context["request"].user
        if game.player != user:
            raise ValidationError("Wrong game_id")
        if game.status != Game.Status.in_progress:
            raise ValidationError("Can't make move in this game")
        self._is_valid_move(game, data["text"])
        return data

    def _is_valid_move(self, game: Game, move: str):
        board = game.get_board()
        try:
            board.parse_uci(move)
        except chess.IllegalMoveError:
            raise ValidationError("Illegal move")

    def save(self, **kwargs):
        game = self.validated_data["game"]
        game.make_move(
            move_uci=self.validated_data["text"],
            source=Move.Source.user
        )
        game.make_bot_move()
        return game
