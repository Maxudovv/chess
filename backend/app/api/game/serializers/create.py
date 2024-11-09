from django.utils import timezone
from rest_framework import serializers

from app.models import Game


class GameCreateSerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Game
        fields = (
            "id",
            "player",
            "colour",
        )

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.status = Game.Status.in_progress
        instance.started_at = timezone.now()
        instance.pgn = '[Site "Chess"]'
        instance.save(update_fields=["status", "started_at", "pgn"])
        if instance.colour == Game.Colour.black:
            instance.perform_stockfish_move()
        return instance
