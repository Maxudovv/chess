from django.urls import path, include

urlpatterns = [
    path("user/", include("app.api.user.urls")),
    path("game/", include("app.api.game.urls"))
]
