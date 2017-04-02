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
        'player1': game.player1,
        'player2': game.player2,
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
