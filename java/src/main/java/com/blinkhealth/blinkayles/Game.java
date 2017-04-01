package com.blinkhealth.blinkayles;

import com.blinkhealth.blinkayles.exceptions.InvalidMoveException;
import com.blinkhealth.blinkayles.exceptions.InvalidTurnException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Game {
    private final Logger logger = LoggerFactory.getLogger(Main.class);

    public static String PLAYER1 = "player1";
    public static String PLAYER2 = "player2";
    public static int PINS = 10;

    Row row;
    String turn;

    public Game() {
        row = new Row(PINS);
        turn = PLAYER1;
    }

    public void move(String player, int pin1, int pin2) throws InvalidTurnException, InvalidMoveException {
        if (!player.equals(turn)) {
            throw new InvalidTurnException();
        }

        row.knockdown(pin1, pin2);
        update_turn();
    }

    public void move(String player, int pin1) throws InvalidTurnException, InvalidMoveException {
        if (!player.equals(turn)) {
            throw new InvalidTurnException();
        }

        row.knockdown(pin1);
        update_turn();
    }

    public void update_turn() {
        if (!isEnded()) {
            if (turn.equals(PLAYER1)) {
                turn = PLAYER2;
            } else {
                turn = PLAYER1;
            }
        }
    }

    public boolean isEnded() {
        return row.getPinsLeft() == 0;
    }

    public String getWinner() {
        if (isEnded()) {
            return turn;
        } else {
            return null;
        }
    }

    public String toString() {
        return row.toString();
    }
}
