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

gameState = new GameState();

$(async function() {
    // exposed functions
    eel.expose(all_change_gamestate);

    function all_change_gamestate(x) {
        update_beamer();
    }

    eel.expose(all_fast_tick);

    function all_fast_tick(timeOver, timeLeft) {
        document.querySelectorAll('.timer').forEach(el => el.innerHTML = timeLeft);
    }

    eel.expose(all_final_tick);

    function all_final_tick(timeOver, timeLeft) {
        document.querySelectorAll('.timer').forEach(el => el.innerHTML = timeLeft);
    }

    function all_show_solution() {
        show_solution();
    }

    eel.expose(all_show_solution);

    async function show_solution() {
        console.log('all_show_solution');
        var current_question = (await eel.get_game()()).current_question;
        document.querySelector('#correctAnswer').innerHTML = current_question.correctAnswer;
        if (current_question.correctAnswer.length > 50) document.querySelector('#slide7').classList.add('smallFont');
        document.querySelector('#chasePlayerResponse').classList.add('show');
        document.querySelector('#chaseChserResponse').classList.add('show');
    }

    function all_show_playerresponse() {
        show_playerresponse();
    }

    eel.expose(all_show_playerresponse);

    async function show_playerresponse() {
        console.log('all_show_playerresponse')
        var current_question = (await eel.get_game()()).current_question;
        if (current_question.answerPlayer == 0) {
            document.querySelector('#chasePlayerResponse').innerHTML = current_question.correctAnswer;
            document.querySelector('#chasePlayerResponse').classList.remove('wrong');
            document.querySelector('#chasePlayerResponse').classList.add('correct');
        } else {
            document.querySelector('#chasePlayerResponse').innerHTML = current_question.wrongAnswers[current_question.answerPlayer - 1];
            document.querySelector('#chasePlayerResponse').classList.remove('correct');
            document.querySelector('#chasePlayerResponse').classList.add('wrong');
        }
        if (document.querySelector('#chasePlayerResponse').innerHTML.length > 50) document.querySelector('#slide7').classList.add('smallFont');
    }

    function all_show_chaserresponse() {
        show_chaserresponse();
    }

    eel.expose(all_show_chaserresponse);

    async function show_chaserresponse() {
        console.log('all_show_chaserresponse')
        var current_question = (await eel.get_game()()).current_question;
        if (current_question.answerChaser == 0) {
            document.querySelector('#chaseChserResponse').innerHTML = current_question.correctAnswer;
            document.querySelector('#chaseChserResponse').classList.remove('wrong');
            document.querySelector('#chaseChserResponse').classList.add('correct');
        } else {
            document.querySelector('#chaseChserResponse').innerHTML = current_question.wrongAnswers[current_question.answerChaser - 1];
            document.querySelector('#chaseChserResponse').classList.remove('correct');
            document.querySelector('#chaseChserResponse').classList.add('wrong');
        }
        if (document.querySelector('#chaseChserResponse').innerHTML.length > 50) document.querySelector('#slide7').classList.add('smallFont');
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
    document.querySelectorAll('audio').forEach(el => {
        el.pause();
        el.load()
    });

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
                var score;
                try {
                    var game = await eel.get_game()();
                    if (game.state != 4) throw (new Error());
                    score = game.current_player.points;
                } catch (e) {
                    clearInterval(fastGuessTimer);
                    //console.error(e);
                    return;
                }
                var oldScore = document.querySelector('#fast_guess_score').innerText;
                document.querySelector('#fast_guess_score').innerHTML = score;
                if (score > oldScore) document.querySelector("#success").play();
            }, 250)
            break;
        case 5: // CHASE_PREPARATION
            if ('fastGuessTimer' in window) clearInterval(fastGuessTimer);

            async function get_offers() {
                try {
                    var offers = (await eel.get_game()()).current_round.offers;
                } catch (e) {
                    clearInterval(offersIntervall);
                    return;
                }
                document.querySelector('#high_offer').innerHTML = offers.find((el) => el.type == 0).amount;
                document.querySelector('#normal_offer').innerHTML = offers.find((el) => el.type == 1).amount;
                document.querySelector('#low_offer').innerHTML = offers.find((el) => el.type == 2).amount;
            }
            offersIntervall = setInterval(get_offers, 250);
            console.log("Jagd Vorbereitung");
            break;
        case 6: // CHASE_QUESTIONING
            if ('offersIntervall' in window) clearInterval(offersIntervall);
            var question = (await eel.get_game()()).current_question;
            document.querySelector('.question').innerHTML = question.text;
            if (question.text.length > 50) document.querySelector('#slide6').classList.add('smallFont');
            else document.querySelector('#slide6').classList.remove('smallFont');

            var correctAnswerButtonOffset = question.correctAnswerButton;
            var buttons = document.querySelector('.option_grid').children;
            for (let i = 0; i < 4; i++) {
                if (i == correctAnswerButtonOffset) {
                    buttons[i].innerHTML = question.correctAnswer;
                } else {
                    buttons[i].innerHTML = question.wrongAnswers[(i < correctAnswerButtonOffset) ? i : i - 1];
                }
                if (buttons[i].innerHTML.length > 50) document.querySelector('#slide6').classList.add('smallFont');
            }
            console.log("Jagd Fragenstellung");
            break;
        case 7: // CHASE_SOLVE
            document.querySelector('#slide7').classList.remove('smallFont');
            document.querySelector('#correctAnswer').innerHTML = '███'
            document.querySelector('#chasePlayerResponse').classList.remove('show');
            document.querySelector('#chaseChserResponse').classList.remove('show');
            document.querySelector('#chasePlayerResponse').innerHTML = '███'
            document.querySelector('#chasePlayerResponse').classList.remove('correct');
            document.querySelector('#chasePlayerResponse').classList.remove('wrong');
            document.querySelector('#chaseChserResponse').innerHTML = '███'
            document.querySelector('#chaseChserResponse').classList.remove('correct');
            document.querySelector('#chaseChserResponse').classList.remove('wrong');
            console.log("Jagd Auflösung");
            break;
        case 8: // ROUND_ENDED
            var player = (await eel.get_game()()).current_player
            document.querySelector((player.qualified) ? '#success' : '#error').play();
            document.querySelector('#playerWonMessage').innerHTML = player.name + ' hat ' + ((player.qualified) ? 'gewonnen' : 'verloren') + '!';
            console.log("Runde beendet");
            break;
        case 9: // FINAL_PREPARATION
            console.log("Finale Vorbereitung");
            break;
        case 10: // FINAL_PLAYERS
            document.querySelector('#finalQuestionPlayer').innerHTML = (await eel.get_game()()).current_question.text
            console.log("Finale Spieler*in");
            break;
        case 11: // FINAL_BETWEEN
            document.querySelector("#waiting").play();
            console.log("Finale Zwischenpause");
            break;
        case 12: // FINAL_CHASER
            document.querySelector('#finalQuestionChaser').innerHTML = (await eel.get_game()()).current_question.text
            console.log("Status: Finale Jäger*in");
            break;
        case 13: // FINAL_CHASER_WRONG
            document.querySelector("#error").play();
            console.log("Finale Jäger*in Falschantwort");
            break;
        case 14: // FINAL_END
            document.querySelector("#waiting").play();
            console.log("Ende");
            break;
        case 15: // EVALUATION
            var game = await eel.get_game()();
            var evaluation = game.current_round;
            document.querySelector('#evaluationMessage').innerHTML = game.current_team.name + ' hat ' + ((evaluation.won) ? 'gewonnen' : 'verloren') + '!';
            document.querySelector('#evaluationScorePlayer').innerHTML = evaluation.correctAnswersPlayer;
            document.querySelector('#evaluationScoreChaser').innerHTML = evaluation.correctAnswersChaser;
            if (evaluation.won) {
                document.querySelector("#success").play();
                document.querySelector('#evaluationScorePlayer').classList.add('correct');
                document.querySelector('#evaluationScorePlayer').classList.remove('wrong');
                document.querySelector('#evaluationScoreChaser').classList.add('wrong');
                document.querySelector('#evaluationScoreChaser').classList.remove('correct');
                document.querySelector("#success").play();
            } else {
                document.querySelector("#error").play();
                document.querySelector('#evaluationScoreChaser').classList.add('correct');
                document.querySelector('#evaluationScoreChaser').classList.remove('wrong');
                document.querySelector('#evaluationScorePlayer').classList.add('wrong');
                document.querySelector('#evaluationScorePlayer').classList.remove('correct');
            }
            console.log("Auswertung");
            break;
        default:
            console.log("Status: Unbekannt " + game.state);
            break;
    }
}