from django.urls import path, include

urlpatterns = [
    path("user/", include("chess.api.user.urls"))
]
