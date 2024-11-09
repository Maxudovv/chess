from rest_framework.generics import CreateAPIView

from app.api.game.serializers.make_move import MakeMoveSerializer
from app.models.game import Move, Game


class MakeMoveAPIView(CreateAPIView):
    queryset = Move.objects.filter(game__status=Game.Status.in_progress)
    serializer_class = MakeMoveSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(player_id=self.request.user.id)
        return queryset
