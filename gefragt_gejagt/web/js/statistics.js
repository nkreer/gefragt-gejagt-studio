class GameState {
    PREPARATION = 0
    TEAM_CHOSEN = 1
    GAME_STARTED = 2
    PLAYER_CHOSEN = 3
    FAST_GUESS = 4
    CHASE_PREPARATION = 5
    CHASE_QUESTIONING = 6
    CHASE_SOLVE = 7
    ROUND_ENDED = 8
    FINAL_PREPARATION = 9
    FINAL_PLAYERS = 10
    FINAL_BETWEEN = 11
    FINAL_CHASER = 12
    FINAL_CHASER_WRONG = 13
    FINAL_END = 14
    EVALUATION = 15

    title(stateCode) {
        switch (stateCode) {
            case this.PREPARATION:
                return 'Vorbereitung'
            case this.TEAM_CHOSEN:
                return 'Team gewählt'
            case this.GAME_STARTED:
                return 'Spiel fängt an'
            case this.PLAYER_CHOSEN:
                return 'Spieler gewählt'
            case this.FAST_GUESS:
                return 'Schnellrate-Runde'
            case this.CHASE_PREPARATION:
                return 'Vorbereitung Jagd'
            case this.CHASE_QUESTIONING:
                return 'Jagdrunde'
            case this.CHASE_SOLVE:
                return 'Jagdrunde Fragenauflösung'
            case this.ROUND_ENDED:
                return 'Runde beendet'
            case this.FINAL_PREPARATION:
                return 'Finale'
            case this.FINAL_PLAYERS:
                return 'Finale Spieler*in'
            case this.FINAL_BETWEEN:
                return 'Finale'
            case this.FINAL_CHASER:
                return 'Finale Jäger*in'
            case this.FINAL_CHASER_WRONG:
                return 'Antwort falsch'
            case this.FINAL_END:
                return 'Finale beendet'
            case this.EVALUATION:
                return 'Auswertung'

            default:
                break;
        }
    }
}

g = new GameState();


async function process_gamestate() {
    let game = await eel.get_game()();

    document.querySelector('#state').innerHTML = g.title(game.state);
    document.querySelector('#state2').innerHTML = g.title(game.state);

    if (game.current_question != null) {
        document.querySelector('#question-text').innerHTML = game.current_question.text;
        // TODO: antwortmoeglichkeiten/antworten anzeigen
    }

    if (game.last_question != null) {
        document.querySelector('#lastquestion-text').innerHTML = game.last_question.text;
        // TODO: antwortmoeglichkeiten/antworten anzeigen
    }

    if (game.current_team != null) {
        document.querySelector('#teamname').innerHTML = game.current_team.name;
        try {
            document.querySelector('#player1name').innerHTML = game.current_team.players[0].name;
            document.querySelector('#player2name').innerHTML = game.current_team.players[1].name;
            document.querySelector('#player3name').innerHTML = game.current_team.players[2].name;
            document.querySelector('#player4name').innerHTML = game.current_team.players[3].name;
        } catch (e) {
            //
        }
    }

    if (game.current_round != null) {
        if (game.current_round.type == 1) {
            document.querySelector('#roundtype').innerHTML = 'Spieler*innenrunde';
        } else {
            document.querySelector('#roundtype').innerHTML = 'Finalrunde';
        }
        document.querySelector('#correctAnswersPlayer').innerHTML = game.current_round.correctAnswersPlayer;
        document.querySelector('#correctAnswersChaser').innerHTML = game.current_round.correctAnswersChaser;

        // TODO: list offers!
    }

    // TODO: simpleQuestionsLeft
    // TODO: chaseQuestionsLeft
}

$(async function() {
    eel.expose(all_change_gamestate);

    function all_change_gamestate(x) {
        process_gamestate();
    }

    eel.expose(all_fast_tick);

    function all_fast_tick(timeOver, timeLeft) {
        document.querySelectorAll('.timer').forEach(el => el.innerHTML = timeLeft);
    }

    eel.expose(all_final_tick);

    function all_final_tick(timeOver, timeLeft) {
        document.querySelectorAll('.timer').forEach(el => el.innerHTML = timeLeft);
    }

    process_gamestate();
});