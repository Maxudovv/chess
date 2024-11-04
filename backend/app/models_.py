# import uuid
#
# from django.contrib.auth.models import User
# from django.db import models
#
#
# class Game(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
#     started_at = models.DateTimeField(null=True)
#     white = models.ForeignKey(User, on_delete=models.PROTECT)
#     black = models.ForeignKey(User, on_delete=models.PROTECT)
#
#     objects = models.Manager()
#
#     class Meta:
#         verbose_name_plural = "Game"
