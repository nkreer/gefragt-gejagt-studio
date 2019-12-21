async function team_table(visible) {
    var tbl = document.getElementById('teamtable');
    if (visible) {
        tbl.style.display = "";

        $("#teamtable tbody tr :visible").remove();
        let teams = await eel.list_teams()()
        for (var i = 0; i < teams.length; i++) {
            var team = teams[i];
            var row = tbl.insertRow(tbl.rows.length);

            row.insertCell(-1).innerHTML = "<input type='button' id='choose_team"+team.id+"' class='button is-link' onclick='eel.choose_team("+team.id+")' value='Spielen'>";
            row.insertCell(-1).innerHTML = team.id;
            row.insertCell(-1).innerHTML = team.name;
            row.insertCell(-1).innerHTML = team.played;
            var playerNames = '';
            team.players.forEach(function(player){
                playerNames += player.name;
                playerNames += ', '
            });
            row.insertCell(-1).innerHTML = playerNames.slice(0,-2);
        }
    } else {
        tbl.style.display = "none";
    }
}

async function question_table(visible, include_all) {
    var tbl = document.getElementById('questiontable');
    if (visible) {
        tbl.style.display = "";

        let game = await eel.get_game()()
        $("#questiontable tbody tr :visible").remove();
        for (var i = 0; i < game.questions.length; i++) {
            var question = game.questions[i];
            if (question.type == 1 && (game.state == 4 || game.state > 9)) {
                var question_matches_round = true;
            } else if (question.type == 2 && (game.state >= 5 && game.state <= 7)) {
                var question_matches_round = true;
            } else {
                var question_matches_round = false;
            }
            if ((question.played || !question_matches_round) && include_all != true) {
                continue;
            }
            var row = tbl.insertRow(-1);

            row.insertCell(-1).innerHTML = "<input type='button' id='choose_question"+question.id+"' class='button is-link' onclick='eel.choose_question("+question.id+")' value='Spielen'>";
            row.insertCell(-1).innerHTML = question.id;
            switch (question.type) {
                case 1:
                    var typetext = "Einfach";
                    break;
                default:
                    var typetext = "Jagd";
                    break;
            }
            row.insertCell(-1).innerHTML = typetext;
            row.insertCell(-1).innerHTML = question.text;
            row.insertCell(-1).innerHTML = question.level;
            row.insertCell(-1).innerHTML = question.played;
            row.insertCell(-1).innerHTML = question.correctAnswer;

            var wrongAnswers = '';
            question.wrongAnswers.forEach(function(wrongAnswer){
                wrongAnswers += wrongAnswer;
                wrongAnswers += ', '
            });
            row.insertCell(-1).innerHTML = wrongAnswers.slice(0,-2);
        }
    } else {
        tbl.style.display = "none";
    }
}

async function player_table(visible, rename_buttons) {
    var tbl = document.getElementById('playertable');
    if (visible) {
        tbl.style.display = "";

        var button = document.getElementById('random-player-btn');

        button.style.display = "";

        $("#playertable tbody tr :visible").remove();
        let game = await eel.get_game()()
        for (var i = 0; i < game.current_team.players.length; i++) {
            var player = game.current_team.players[i];
            var row = tbl.insertRow(tbl.rows.length);

            if (rename_buttons == true) {
                row.insertCell(-1).innerHTML = "<input type='button' id='choose_player"+player.id+"' class='button is-link' onclick='eel.choose_player("+player.id+")' value='De-/Qualifizieren'>";
            } else {
                row.insertCell(-1).innerHTML = "<input type='button' id='choose_player"+player.id+"' class='button is-link' onclick='eel.choose_player("+player.id+")' value='Spielen'>";
            }
            row.insertCell(-1).innerHTML = player.id;
            row.insertCell(-1).innerHTML = player.name;
            row.insertCell(-1).innerHTML = player.points;
            row.insertCell(-1).innerHTML = player.level;
            row.insertCell(-1).innerHTML = player.played;
            row.insertCell(-1).innerHTML = player.qualified;
        }
    } else {
        tbl.style.display = "none";
    }
}

function notification(visible, text) {
    var notification = document.getElementById('notification');
    notification.innerHTML = text;
    if (visible) {
        notification.style.display = "";
    } else {
        notification.style.display = "none";
    }
};

function endtext(visible, text) {
    var endtext = document.getElementById('endtext');
    endtext.innerHTML = text;
    if (visible) {
        endtext.style.display = "";
    } else {
        endtext.style.display = "none";
    }
};

function team_message(visible, text) {
    var message = document.getElementById('team-message');
    message.children[1].innerHTML = text;
    if (visible) {
        message.style.display = "";
    } else {
        message.style.display = "none";
    }
};

function player_message(visible, text) {
    var message = document.getElementById('player-message');
    message.children[1].innerHTML = text;
    if (visible) {
        message.style.display = "";
    } else {
        message.style.display = "none";
    }
};

function question_message(visible, question) {
    // TODO: Add keyboard shortcuts
    var message = document.getElementById('question-message');
    if (visible) {
        message.children[1].innerHTML = question.text;

        var buttons2 = '';
        if (question.type == 1) {
            // FAST
            var buttons = '<a onclick="eel.question_answered(0)" class="card-footer-item">'+question.correctAnswer+'</a><a onclick="eel.question_answered(1)" class="card-footer-item is-warning">Falche Antwort</a>'

            message.children[3].display = "none";
        } else {
            // NORMAL
            var buttons = '<p class="card-footer-item">Spieler</p><a onclick="eel.question_answered(0,0)" class="card-footer-item">'+question.correctAnswer+'</a>';
            var buttons2 = '<p class="card-footer-item">Jäger</p><a onclick="eel.question_answered(0,1)" class="card-footer-item">'+question.correctAnswer+'</a>';
            for (var i = 0; i < question.wrongAnswers.length; i++) {
                var answer = question.wrongAnswers[i];
                buttons += '<a onclick="eel.question_answered('+ (i+1) +',0)" class="card-footer-item">'+answer+'</a>'
                buttons2 += '<a onclick="eel.question_answered('+ (i+1) +',1)" class="card-footer-item">'+answer+'</a>'
            }
            message.children[3].style.display = "";
        }
        message.children[2].innerHTML = buttons;
        message.children[3].innerHTML = buttons2;

        message.style.display = "";
    } else {
        message.style.display = "none";
    }
};

function final_start_message(visible, chaser, game) {
    var message = document.getElementById('final-start-message');
    var button = document.getElementById('final-start-message-button');

    if (visible) {
        if (!chaser) {
            var playerNames = '';
            game.current_team.players.forEach(function(player){
                if (player.qualified) {
                    playerNames += player.name;
                    playerNames += ', ';
                }
            });
            message.children[1].innerHTML = 'Mit ' + playerNames.slice(0,-2);

            button.setAttribute('onclick', "eel.start_final_game()")
        } else {
            message.children[0].children[0].innerHTML = 'Finalrunde; Jäger*in';
            message.children[1].innerHTML = 'Spielstand, Spieler: ' + (game.current_round.playerStartOffset +
                  game.current_round.correctAnswersPlayer);

            button.setAttribute('onclick', "eel.start_final_chaser()")
        }

        message.style.display = "";
    } else {
        message.style.display = "none";
    }
};

function offer_card(visible, game) {
    var card = document.getElementById('offer-card');
    // offer-high-points
    if (visible) {
        card.style.display = "";

        $('#offer-high-points').val(game.current_round.offers[0].amount);
        $('#offer-normal-points').val(game.current_round.offers[1].amount);
        $('#offer-low-points').val(game.current_round.offers[2].amount);
    } else {
        card.style.display = "none";
    }
};

function solution_card(visible, game) {
    var card = document.getElementById('solution-card');
    // offer-high-points
    if (visible) {
        card.style.display = "";
        card.children[1].children[0].innerHTML = "<strong>Frage:</strong> "+game.current_question.text+"<br><br>";
        card.children[1].children[0].innerHTML += "<strong>Richtige Antwort:</strong> "+game.current_question.correctAnswer+"<br>";
        if (game.current_question.answerPlayer == 0) {
            var playerAnswerText = game.current_question.correctAnswer;
            var playerAnswerRating = '<span class="tag is-success">Richtig</span>';
        } else {
            var playerAnswerText = game.current_question.wrongAnswers[game.current_question.answerPlayer-1];
            var playerAnswerRating = '<span class="tag is-danger">Falsch</span>';
        }
        card.children[1].children[0].innerHTML += "<strong>Spielerantwort:</strong> "+playerAnswerText+" "+playerAnswerRating+"<br>";
        if (game.current_question.answerChaser == 0) {
            var chaserAnswerText = game.current_question.correctAnswer;
            var chaserAnswerRating = '<span class="tag is-success">Richtig</span>';
        } else {
            var chaserAnswerText = game.current_question.wrongAnswers[game.current_question.answerChaser-1];
            var chaserAnswerRating = '<span class="tag is-danger">Falsch</span>';
        }
        card.children[1].children[0].innerHTML += "<strong>Jägerantwort:</strong> "+chaserAnswerText+"  "+chaserAnswerRating+"<br>";
    } else {
        card.style.display = "none";
    }
};

function set_offer(input_nr) {
    var input_amount = 0;
    switch (input_nr) {
        case 0:
            input_amount = $("#offer-high-points").val();
            break;
        case 2:
            input_amount = $("#offer-low-points").val();
            break;
        default:
            input_amount = $("#offer-normal-points").val();
            break;
    }
    eel.set_offer(input_nr, input_amount);
}

async function load_filenames() {
    let files = await eel.get_files()();
    $("#file-picker option").remove();

    files = files.reverse();

    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        $("#file-picker").append('<option value=' + file + '>' + file + '</option>');
    }
}

function send_load_game() {
    console.log($("#file-picker").val());
    eel.load_game($("#file-picker").val());
}

async function process_gamestate() {
    let game = await eel.get_game()();

    team_table(false);
    team_message(false);
    player_table(false);
    player_message(false);
    question_table(false);
    question_message(false);
    offer_card(false);
    solution_card(false);
    endtext(false);
    final_start_message(false);

    switch (game.state) {
        case 0:  // PREPARATION
            document.getElementById("status").innerHTML = "Status: Vorbereitung";
            team_table(true);
            break;
        case 1:  // TEAM_CHOSEN
            document.getElementById("status").innerHTML = "Status: Team ausgewählt";
            team_table(true);
            team_message(true, game.current_team.name);
            break;
        case 2:  // GAME_STARTED
            document.getElementById("status").innerHTML = "Status: Spiel gestartet";
            player_table(true, false);
            break;
        case 3:  // PLAYER_CHOSEN
            document.getElementById("status").innerHTML = "Status: Spieler ausgewählt";
            player_table(true, false);
            player_message(true, game.current_player.name);
            break;
        case 4:  // FAST_GUESS
            document.getElementById("status").innerHTML = "Status: Schnellraterunde";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 5:  // CHASE_PREPARATION
            document.getElementById("status").innerHTML = "Status: Jagd Vorbereitung";
            offer_card(true, game);
            break;
        case 6:  // CHASE_QUESTIONING
            document.getElementById("status").innerHTML = "Status: Jagd Fragenstellung";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 7:  // CHASE_SOLVE
            document.getElementById("status").innerHTML = "Status: Jagd Auflösung";
            question_table(true);
            solution_card(true, game);
            break;
        case 8:  // ROUND_ENDED
            document.getElementById("status").innerHTML = "Status: Runde beendet";
            $('#timer').text("");
            if (game.current_player.qualified) {
                endtext(true,game.current_player.name + ` hat gewonnen!
                    <br>
                    <br>
                    <a class="button is-info" onclick="eel.end_round()">
                    Runde beenden
                    </a>
                `);
            } else {
                endtext(true,game.current_player.name + ` hat verloren!
                    <br>
                    <br>
                    <a class="button is-info" onclick="eel.end_round()">
                    Runde beenden
                    </a>
                `);
            }
            break;
        case 9:  // FINAL_PREPARATION
            document.getElementById("status").innerHTML = "Status: Finale Vorbereitung";
            $('#timer').text("");
            player_table(true, true);
            if(game.current_team.qualified) {
                final_start_message(true, false, game);
            }
            break;
        case 10:  // FINAL_PLAYERS
            document.getElementById("status").innerHTML = "Status: Finale Spieler*in";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 11:  // FINAL_BETWEEN
            document.getElementById("status").innerHTML = "Status: Finale Zwischenpause";
            $('#timer').text("");
            final_start_message(true, true, game);
            break;
        case 12:  // FINAL_CHASER
            document.getElementById("status").innerHTML = "Status: Finale Jäger*in";
            question_table(true);
            question_message(true, game.current_question);
            break;
        case 13:  // FINAL_CHASER_WRONG
            document.getElementById("status").innerHTML = "Status: Finale Jäger*in Falschantwort";
            question_message(true, game.current_question);
            break;
        case 14:  // FINAL_END
            document.getElementById("status").innerHTML = "Status: Ende";
            $('#timer').text("");
            break;
        case 15:  // EVALUATION
            document.getElementById("status").innerHTML = "Status: Auswertung";
            $('#timer').text("");
            break;
        default:
            document.getElementById("status").innerHTML = "Status: Unbekannt; "+game.state;
            break;
    }
}

$(async function() {

    // exposed functions
    eel.expose(dashboard_set_heading);
    function dashboard_set_heading(x) {
        $('#heading').text(x);
    }

    eel.expose(all_change_gamestate);
    function all_change_gamestate(x) {
        process_gamestate();
    }

    eel.expose(dashboard_set_url);
    function dashboard_set_url(url) {
        window.location.href = url;
    }

    eel.expose(all_fast_tick);
    function all_fast_tick(time_played, time_remaining) {
        $('#timer').text(time_remaining + " Sekunden verbleibend");
    }

    eel.expose(all_fast_timeout);
    function all_fast_timeout(time) {
        $('#timer').text("");
    }

    eel.expose(all_chase_tick);
    function all_chase_tick(time_played, time_remaining) {
        $('#timer').text(time_remaining + " Sekunden verbleibend");
    }

    eel.expose(all_chase_timeout);
    function all_chase_timeout(time) {
        $('#timer').text("");
    }

    eel.expose(all_chase_both_answered);
    function all_chase_both_answered(time) {
        $('#timer').text("");
    }

    eel.expose(all_final_tick);
    function all_final_tick(time_played, time_remaining) {
        $('#timer').text(time_remaining + " Sekunden verbleibend");
    }

    eel.expose(all_final_pause);
    function all_final_pause(time_played, time_remaining) {
        $('#timer').text("Frage pausiert; " + time_remaining + " Sekunden verbleibend");
    }

    eel.expose(all_final_timeout);
    function all_final_timeout(time) {
        $('#timer').text("");
    }

    eel.expose(all_new_question);
    function all_new_question() {
        //nothing
    }

    // onload functionallity
    process_gamestate();
});
