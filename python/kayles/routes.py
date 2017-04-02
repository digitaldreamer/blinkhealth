import json
import logging

from flask import (
    Blueprint,
    make_response,
    jsonify,
    request,
)
from kayles import exceptions
from kayles.models import (
    game,
    tournament,
    Game,
    Tournament,
)

logger = logging.getLogger(__name__)
routes = Blueprint('game', __name__)


@routes.errorhandler(exceptions.GameException)
def all_exception_handler(error):
    data = {
        'message': '{}: {}'.format(error.__class__.__name__, str(error))
    }
    return make_response(jsonify(data), 400)

@routes.route('/game', methods=['POST'])
def new_game():
    global game
    args = request.json or {}
    player1 = args.get('player1')
    player2 = args.get('player2')

    # validate
    if not player1 or not player2:
        data = {
            'message': 'ERROR: need both player1 and player2'
        }
        return make_response(jsonify(data), 400)

    game = Game(player1, player2)
    data = {
        'message': 'new game started',
    }
    logger.info('started new game player1:%s player2:%s', game.player1, game.player2)
    return make_response(jsonify(data), 201)


@routes.route('/move/<player>/<int:pin1>', methods=['POST'], defaults={'pin2': None})
@routes.route('/move/<player>/<int:pin1>,<int:pin2>', methods=['POST'])
def move(player, pin1, pin2):
    if not game or game.is_ended():
        data = {
            'message': 'No active game. POST /game to start a new game.'
        }
        return make_response(jsonify(data), 400)

    game.move(player, pin1, pin2)
    if game.is_ended():
        message = '{} is the winner!'.format(game.get_winner())
    else:
        message = game.__str__()

    data = {
        'message': message,
    }
    return make_response(jsonify(data), 201)


@routes.route('/tournament', methods=['GET'])
def get_tournament():
    if tournament == None:
        data = {
            'message': 'no active tournament',
        }
        return make_response(jsonify(data), 404)

    data = tournament_data()
    return make_response(jsonify(data), 200)


def tournament_data():
    data = {
        'players': {
            'active': tournament.get_players(True),
            'removed': tournament.get_players(False),
        }
    }

    if tournament.winner:
        data['winner'] = tournament.winner

    return data


@routes.route('/tournament', methods=['POST'])
def new_tournament():
    global tournament
    args = request.json or {}
    players = args.get('players', [])

    # validate
    if not len(players) > 2:
        data = {
            'message': 'ERROR: need at least 3 players to start a tournament'
        }
        return make_response(jsonify(data), 400)

    tournament = Tournament(players=players)
    logger.info('started new tournament with %s players', len(players))

    data = tournament_data()
    return make_response(jsonify(data), 201)


@routes.route('/tournament/players/<player>', methods=['DELETE'])
def remove_player(player):
    if tournament == None:
        data = {
            'message': 'no active tournament',
        }
        return make_response(jsonify(data), 400)

    tournament.remove_player(player)
    logger.info('player:%s removed from tournament', player)

    data = tournament_data()
    return make_response(jsonify(data), 201)
