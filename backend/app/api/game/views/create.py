from rest_framework.generics import CreateAPIView

from app.api.game.serializers.create import GameCreateSerializer
from app.models import Game


class StartNewGameAPIView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameCreateSerializer
