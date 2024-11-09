from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from app.models import Game


class ResignGameAPIView(GenericAPIView):
    queryset = Game.objects.filter(status=Game.Status.in_progress)
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(player_id=self.request.user.id)
        return queryset

    def get_object(self):
        self.kwargs["id"] = self.request.data.get("game")
        return super().get_object()

    def post(self, request, *args, **kwargs):
        instance: Game = self.get_object()
        instance.perform_resignation()
        return Response(status=200)
