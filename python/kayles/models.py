class GameException(Exception): pass
class InvalidMoveException(GameException): pass
class InvalidTurnException(GameException): pass


game = None
tournament = None


class Game(object):
    PINS = 10
    player1 = ''
    player2 = ''

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.row = Row(self.PINS)
        self.turn = self.player1

    def move(self, player, pin1, pin2=None):
        if player != self.turn:
            raise InvalidTurnException()

        self.row.knockdown(pin1, pin2)
        self.update_turn()

    def update_turn(self):
        if self.is_ended():
            return

        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def is_ended(self):
        return self.row.get_pins_left() == 0

    def get_winner(self):
        if self.is_ended():
            return self.turn
        else:
            return None

    def __str__(self):
        return self.row.__str__()


class Row(object):
    def __init__(self, length):
        self.pins = [True for i in range(length)]

    def __str__(self):
        return ''.join(['!' if x else 'x' for x in self.pins])

    def knockdown(self, index1, index2=None):
        try:
            if not self.pins[index1]:
                raise InvalidMoveException()

            self.pins[index1] = False

            if index2:
                if abs(index1 - index2) != 1:
                    raise InvalidMoveException()

                if not self.pins[index2]:
                    raise InvalidMoveException()

                self.pins[index2] = False
        except IndexError:
            raise InvalidMoveException()

    def get_pins_left(self):
        return self.pins.count(True)
