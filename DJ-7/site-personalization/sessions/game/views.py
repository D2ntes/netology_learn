from django.shortcuts import render, redirect
import random
from django import http

from .models import Player, Game
from .forms import GameFormPost
from .settings import MAX_NUMBER, MIN_NUMBER


def show_home(request):
    data = dict()

    user_id = request.session.session_key
    if not user_id:
        request.session.cycle_key()
        user_id = request.session.session_key

    player = Player.objects.filter(player_id=user_id).first()
    if not player:
        player = Player.objects.create(player_id=user_id)

    games = Game.objects.filter(is_finished=False)
    done_games = games.filter(is_active=False)
    if done_games:
        game = done_games.first()
        data['try_count'] = game.try_count
        game.is_finished = True
        game.save()
    else:
        if not games:
            random_num = random.randint(MIN_NUMBER, MAX_NUMBER)
            game = Game.objects.create(owner=player, num=random_num)
            game.players.add(player)
            data['random_num'] = game.num
        else:
            game = games.first()
            if game.owner != player:
                game.players.add(player)
                data['form'] = GameFormPost(request.POST)
            else:
                data['random_num'] = game.num

    if request.method == 'POST':
        num = int(request.POST.get('number'))
        true_num = int(game.num)

        if num > true_num:
            data['tip'] = "Вы ввели слишком большое число!"
            game.try_count += 1
            game.save()
        elif num < true_num:
            game.try_count += 1
            game.save()
            data['tip'] = "Вы ввели слишком маленькое число!"
        elif num == true_num:
            game.try_count += 1
            game.is_active = False
            game.save()
            return redirect('home')

    return render(
        request,
        'home.html',
        context=data
    )
