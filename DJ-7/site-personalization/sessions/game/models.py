from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=255, default='Игрок', verbose_name='ID игрока')


class Game(models.Model):
    players = models.ManyToManyField(Player, related_name='games')
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)
    is_finished = models.BooleanField(default=False)
    try_count = models.IntegerField(default=0)
    num = models.IntegerField(default=0)


class PlayerGameInfo(models.Model):
    pass
