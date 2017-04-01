# Blinkayles

Blinkayles is a REST implementation of Kayles, the simple two-player math game. From [Wikipedia](https://en.wikipedia.org/wiki/Kayles):

> Kayles is played with a row of tokens, which represent bowling pins. The row may be of any length. The two players alternate; each player, on his or her turn, may remove either any one pin (a ball bowled directly at that pin), or two adjacent pins (a ball bowled to strike both). Under the normal play convention, a player loses when he or she has no legal move (that is, when all the pins are gone). The game can also be played using misère rules; in this case, the player who cannot move wins.

This variation uses misère rules: the last player to knock down a pin wins.

### POST `/game`

Begin a new game

### POST `/move/<player>/<pin>[,<pin>]`

Knock down one or two pins
