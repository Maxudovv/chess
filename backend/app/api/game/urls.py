from django.urls import path

from app.api.game.views.create import StartNewGameAPIView
from app.api.game.views.make_move import MakeMoveAPIView
from app.api.game.views.resign import ResignGameAPIView

urlpatterns = [
    path("start", StartNewGameAPIView.as_view()),
    path("make_move", MakeMoveAPIView.as_view()),
    path("resign", ResignGameAPIView.as_view()),
]
