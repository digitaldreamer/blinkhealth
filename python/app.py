from flask import Flask
from game import Game, GameException

app = Flask(__name__)
game = None


@app.route('/game', methods=['POST'])
def new_game():
    global game
    game = Game()
    return '''Game started!
The player who knocks down the last pin wins.
Players: {}, {}
Pins: {}'''.format(Game.PLAYER1, Game.PLAYER2, Game.PINS), 201


@app.route('/move/<player>/<int:pin1>', methods=['POST'], defaults={'pin2': None})
@app.route('/move/<player>/<int:pin1>,<int:pin2>', methods=['POST'])
def move(player, pin1, pin2):
    if not game or game.is_ended():
        return 'No active game. POST /game to start a new game.', 400

    game.move(player, pin1, pin2)
    if game.is_ended():
        return '{} is the winner!'.format(game.get_winner())
    else:
        return game.__str__()


@app.errorhandler(GameException)
def all_exception_handler(error):
    return error.__class__.__name__, 400


if __name__ == '__main__':
    print 'POST /game to start a new game'
    app.run(debug=True)
