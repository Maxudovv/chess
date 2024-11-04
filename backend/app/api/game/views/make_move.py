from rest_framework.generics import CreateAPIView

from app.api.game.serializers.make_move import MakeMoveSerializer
from app.models.game import Move


class MakeMoveAPIView(CreateAPIView):
    queryset = Move.objects.all()
    serializer_class = MakeMoveSerializer
