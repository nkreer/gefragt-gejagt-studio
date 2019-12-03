async function team_table(visible) {
    var tbl = document.getElementById('teamtable');
    if (visible) {
        tbl.style.display = "";

        $("#teamtable tbody tr :visible").remove();
        let teams = await eel.list_teams()()
        for (var i = 0; i < teams.length; i++) {
            var team = teams[i];
            var row = tbl.insertRow(tbl.rows.length);

            row.insertCell(0).innerHTML = "<input type='button' id='choose_team"+team.id+"' class='button is-link' onclick='eel.choose_team("+team.id+")' value='Spielen'>";
            row.insertCell(1).innerHTML = team.id;
            row.insertCell(2).innerHTML = team.name;
            var playerNames = '';
            team.players.forEach(function(player){
                playerNames += player.name;
                playerNames += ', '
            });
            row.insertCell(3).innerHTML = playerNames.slice(0,-2);
        }
    } else {
        tbl.style.display = "none";
    }
}

async function question_table(visible, include_all) {
    var tbl = document.getElementById('questiontable');
    if (visible) {
        tbl.style.display = "";

        $("#questiontable tbody tr :visible").remove();
        let game = await eel.get_game()()
        for (var i = 0; i < game.questions.length; i++) {
            var question = game.questions[i];
            if (question.type == 1 && (game.state == 4 || game.state == 8)) {
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

            //$('#myTable > tbody:last').append()
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

async function player_table(visible) {
    var tbl = document.getElementById('playertable');
    if (visible) {
        tbl.style.display = "";

        $("#playertable tbody tr :visible").remove();
        let game = await eel.get_game()()
        for (var i = 0; i < game.current_team.players.length; i++) {
            var player = game.current_team.players[i];
            var row = tbl.insertRow(tbl.rows.length);

            row.insertCell(0).innerHTML = "<input type='button' id='choose_player"+player.id+"' class='button is-link' onclick='eel.choose_player("+player.id+")' value='Spielen'>";
            row.insertCell(1).innerHTML = player.id;
            row.insertCell(2).innerHTML = player.name;
            row.insertCell(3).innerHTML = player.points;
            row.insertCell(4).innerHTML = player.level;
            row.insertCell(5).innerHTML = player.played;
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
        if (question.type == 1) {
            // FAST
            var buttons = '<a onclick="eel.question_answered(0)" class="card-footer-item">'+question.correctAnswer+'</a><a onclick="eel.question_answered(1)" class="card-footer-item is-warning">Falche Antwort</a>'
        } else {
            // NORMAL
            var buttons = '<a onclick="eel.question_answered(0)" class="card-footer-item">'+question.correctAnswer+'</a>';
            for (var i = 0; i < question.wrongAnswers.length; i++) {
                var answer = question.wrongAnswers[i];
                buttons += '<a onclick="eel.question_answered('+ (i+1) +')" class="card-footer-item">'+answer+'</a>'
            }
        }
        message.children[2].innerHTML = buttons;
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

async function process_gamestate() {
    let game = await eel.get_game()();

    team_table(false);
    team_message(false);
    player_table(false);
    player_message(false);
    question_table(false);
    question_message(false);
    offer_card(false);

    set_modal(false, 'reset-modal');

    switch (game.state) {
        case 0:  // PREPARATION
            team_table(true);
            document.getElementById("status").innerHTML = "Status: Vorbereitung";
            break;
        case 1:  // TEAM_CHOSEN
            team_table(true);
            team_message(true, game.current_team.name);
            document.getElementById("status").innerHTML = "Status: Team ausgewählt";
            break;
        case 2:  // GAME_STARTED
            player_table(true);
            document.getElementById("status").innerHTML = "Status: Spiel gestartet";
            break;
        case 3:  // PLAYER_CHOSEN
            player_table(true);
            player_message(true, game.current_player.name);
            document.getElementById("status").innerHTML = "Status: Spieler ausgewählt";
            break;
        case 4:  // FAST_GUESS
            question_table(true);
            question_message(true, game.current_question);
            document.getElementById("status").innerHTML = "Status: Schnellraterunde";
            break;
        case 5:  // CHASE_PREPARATION
            offer_card(true, game);
            document.getElementById("status").innerHTML = "Status: Jagd Vorbereitung";
            break;
        case 6:  // CHASE_QUESTIONING
            question_table(true);
            question_message(true, game.current_question);
            document.getElementById("status").innerHTML = "Status: Jagd Fragenstellung";
            break;
        case 7:  // CHASE_SOLVE
            question_table(true);
            question_message(true, game.current_question);
            document.getElementById("status").innerHTML = "Status: Jagd Auflösung";
            break;
        default:
            question_table(true);
            document.getElementById("status").innerHTML = "Status: Unbekannt";
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

    // onload functionallity
    process_gamestate();
});
