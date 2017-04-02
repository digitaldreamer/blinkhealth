# Blinkayles

Blinkayles is a REST implementation of Kayles, the simple two-player math game. From [Wikipedia](https://en.wikipedia.org/wiki/Kayles):

> Kayles is played with a row of tokens, which represent bowling pins. The row may be of any length. The two players alternate; each player, on his or her turn, may remove either any one pin (a ball bowled directly at that pin), or two adjacent pins (a ball bowled to strike both). Under the normal play convention, a player loses when he or she has no legal move (that is, when all the pins are gone). The game can also be played using misère rules; in this case, the player who cannot move wins.

This variation uses misère rules: the last player to knock down a pin wins.


# Install

I implemented the python version using python3.

It is built as a pip-installable package and `kayles` is required to be in the python path.

Run the following commands to initialize the virtualenv and install dependencies

```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
python3 setup.py develop
```

# Run

```
python3 kayles/app.py
```

# Simulate Game (deprecated)

NOTE: changes were made to the endpoints play.sh calls
You can simulate playing a game with `play.sh`:

```
play.sh
```

# Make commands

To get the list of make targets run:

```
make help
```

### API Documentation

I used postman to interact with all routes and to provide documentation

https://documenter.getpostman.com/view/9825/blinkhealth/6YvVbhF
