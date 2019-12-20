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
                return 'Jagdrunde'
            case this.ROUND_ENDED:
                return 'Runde beendet'
            case this.FINAL_PREPARATION:
                return 'Vorbereitung Finale'
            case this.FINAL_PLAYERS:
                return 'Auswahl Finalspieler'
            case this.FINAL_BETWEEN:
                return 'Frage wählen'
            case this.FINAL_CHASER:
                return 'Antwort richtig'
            case this.FINAL_CHASER_WRONG:
                return 'Antwort falsch'
            case this.FINAL_END:
                return 'Finalrunde beendet'
            case this.EVALUATION:
                return 'Auswertung'

            default:
                break;
        }
    }
}

gameState = new GameState();

$(async function() {
    // exposed functions
    eel.expose(all_change_gamestate);

    function all_change_gamestate(x) {
        update_beamer();
    }

    eel.expose(all_fast_tick);

    function all_fast_tick(timeOver, timeLeft) {
        document.querySelectorAll('.fast_guess_timer').forEach(el => el.innerHTML = timeLeft);
    }

    // Init
    update_beamer();
});

async function update_beamer() {
    gameStateCode = await eel.game_state()();

    document.querySelector("#GAME_STATE").innerHTML = gameState.title(gameStateCode)

    document.querySelectorAll('section').forEach(el => (el.id != 'slide' + gameStateCode) ? el.classList.remove('active') : el.classList.add('active'))

    loadSlideContent(gameStateCode)
}

async function loadSlideContent(gameStateCode) {

    switch (gameStateCode) {
        case gameState.PREPARATION: // PREPARATION
            document.querySelector('.logo_container').classList.add('fullscreen')
            console.log("Vorbereitung");
            break;
        case gameState.TEAM_CHOSEN: // TEAM_CHOSEN
            document.querySelector('.logo_container').classList.remove('fullscreen');
            document.querySelector('#selected_team_name').innerHTML = (await eel.get_game()()).current_team.name
            console.log("Team ausgewählt");
            break;
        case 2: // GAME_STARTED
            console.log("Spiel gestartet");
            break;
        case 3: // PLAYER_CHOSEN
            console.log("Spieler ausgewählt");
            document.querySelector('#player_name').innerHTML = (await eel.get_game()()).current_player.name
            break;
        case 4: // FAST_GUESS
            console.log("Schnellraterunde");
            fastGuessTimer = setInterval(async function() {
                var score = (await eel.get_game()()).current_player.points;
                document.querySelectorAll('.fast_guess_score').forEach(el => el.innerHTML = score);
            }, 250)
            break;
        case 5: // CHASE_PREPARATION
            if ('fastGuessTimer' in window) clearInterval(fastGuessTimer);

            async function get_offers() {
                var offers = (await eel.get_game()()).current_round.offers;
                document.querySelector('#high_offer').innerHTML = offers.find((el) => el.type == 0).amount;
                document.querySelector('#normal_offer').innerHTML = offers.find((el) => el.type == 1).amount;
                document.querySelector('#low_offer').innerHTML = offers.find((el) => el.type == 2).amount;
            }
            offersIntervall = setInterval(get_offers, 250);
            console.log("Jagd Vorbereitung");
            break;
        case 6: // CHASE_QUESTIONING
            if ('offersIntervall' in window) clearInterval(offersIntervall);
            async function loadQuestion() {
                var question = (await eel.get_game()()).current_question;
                document.querySelector('.question').innerHTML = question.text;

                var correctAnswerButtonOffset = Math.round(Math.random() * 3);
                var buttons = document.querySelector('.option_grid').children;
                for (let i = 0; i < 4; i++) {
                    if (i == correctAnswerButtonOffset) {
                        buttons[i].innerHTML = question.correctAnswer;
                    } else {
                        buttons[i].innerHTML = question.wrongAnswers[(i < correctAnswerButtonOffset) ? i : i - 1];
                    }
                }
            }
            loadQuestion();
            console.log("Jagd Fragenstellung");
            break;
        case 7: // CHASE_SOLVE
            document.getElementById("status").innerHTML = "Status: Jagd Auflösung";
            question_table(true);
            solution_card(true, game);
            break;
        case 8: // ROUND_ENDED
            document.getElementById("status").innerHTML = "Status: Runde beendet";
            if (game.current_player.qualified) {
                endtext(true, game.current_player.name + ` hat gewonnen!
                    <br>
                    <br>
                    <a class="button is-info" onclick="eel.end_round()">
                    Runde beenden
                    </a>
                `);
            } else {
                endtext(true, game.current_player.name + ` hat verloren!
                    <br>
                    <br>
                    <a class="button is-info" onclick="eel.end_round()">
                    Runde beenden
                    </a>
                `);
            }
            break;
        case 9: // FINAL_PREPARATION
            document.getElementById("status").innerHTML = "Status: Finale Vorbereitung";
            player_table(true, true);
            if (game.current_team.qualified) {
                final_start_message(true, false, game);
            }
            break;
        case 10: // FINAL_PLAYERS
            document.getElementById("status").innerHTML = "Status: Finale Spieler*in";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 11: // FINAL_BETWEEN
            document.getElementById("status").innerHTML = "Status: Finale Zwischenpause";
            final_start_message(true, true, game);
            break;
        case 12: // FINAL_CHASER
            document.getElementById("status").innerHTML = "Status: Finale Jäger*in";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 13: // FINAL_CHASER_WRONG
            document.getElementById("status").innerHTML = "Status: Finale Jäger*in Falschantwort";
            break;
        case 14: // FINAL_END
            document.getElementById("status").innerHTML = "Status: Ende";
            break;
        case 15: // EVALUATION
            document.getElementById("status").innerHTML = "Status: Auswertung";
            break;
        default:
            document.getElementById("status").innerHTML = "Status: Unbekannt " + game.state;
            break;
    }
}