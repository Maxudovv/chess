from django.contrib import admin

from app.models import Game
from app.models.game import Move

# Register your models here.
admin.site.register(Game)
admin.site.register(Move)