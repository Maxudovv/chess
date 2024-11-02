from rest_framework.generics import CreateAPIView

from backend.chess.models import Game


class CreateGameAPIView(CreateAPIView):
    queryset = Game.objects.all()
    def create(self, request, *args, **kwargs):
        pass