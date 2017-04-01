package com.blinkhealth.blinkayles;

import com.blinkhealth.blinkayles.exceptions.GameException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import spark.Request;
import static spark.Spark.before;
import static spark.Spark.exception;
import static spark.Spark.post;

public class Main {
    private final static Logger logger = LoggerFactory.getLogger(Main.class);
    private static Game currentGame;

    private static String requestInfoToString(Request request) {
        StringBuilder sb = new StringBuilder();
        sb.append(request.requestMethod());
        sb.append(" " + request.url());
        sb.append(" " + request.body());
        return sb.toString();
    }

    public static void main(String[] args) {
        before((request, response) -> {
            logger.info(requestInfoToString(request));
        });

        exception(GameException.class, (exception, request, response) -> {
            response.status(400);
            response.body(exception.getClass().getSimpleName());
        });

        post("/game", (request, response) -> {
            currentGame = new Game();
            String template = "Game started! The player who knocks down the last pin wins.  Players: %s %s Pins: %d";
            return String.format(template, Game.PLAYER1, Game.PLAYER2, Game.PINS);
        });

        post("/move/:player/:pins", (request, response) -> {
            String[] pins = request.params("pins").split(",");
            String player = request.params("player");

            if (currentGame == null || currentGame.isEnded()) {
                return "No active game.  call new game to start a new game.";
            }

            if (pins.length == 1) {
                currentGame.move(player, Integer.parseInt(pins[0]));
            } else if (pins.length == 2) {
                currentGame.move(player, Integer.parseInt(pins[0]), Integer.parseInt(pins[1]));
            }

            if (currentGame.isEnded()) {
                return String.format("%s is the winner!", currentGame.getWinner());
            } else {
                return currentGame.toString();
            }
        });
    }
}


