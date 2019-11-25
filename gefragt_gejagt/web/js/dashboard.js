async function team_table(visible) {
    var tbl = document.getElementById('teamtable');
    if (visible) {
        tbl.style.display = "";

        if (tbl.rows.length <= 1) {
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
        }
    } else {
        tbl.style.display = "none";
    }
}

async function question_table(visible) {
    var tbl = document.getElementById('questiontable');
    if (visible) {
        tbl.style.display = "";

        if (tbl.rows.length <= 1) {
            let game = await eel.get_game()()
            for (var i = 0; i < game.questions.length; i++) {
                var question = game.questions[i];
                var row = tbl.insertRow(tbl.rows.length);

                row.insertCell(0).innerHTML = "<input type='button' id='choose_question"+question.id+"' class='button is-link' onclick='eel.choose_question("+question.id+")' value='Spielen'>";
                row.insertCell(1).innerHTML = question.id;
                row.insertCell(2).innerHTML = question.text;
                row.insertCell(3).innerHTML = question.correctAnswer;

                var wrongAnswers = '';
                question.wrongAnswers.forEach(function(wrongAnswer){
                    wrongAnswers += wrongAnswer;
                    wrongAnswers += ', '
                });
                row.insertCell(4).innerHTML = wrongAnswers.slice(0,-2);
            }
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

async function process_gamestate() {
    let game = await eel.get_game()();
    if (game.state == 0){
        // PREPARATION
        team_table(true);
        team_message(false);
        question_table(false);
        document.getElementById("status").innerHTML = "Status: Vorbereitung";
    } else if (game.state == 1) {
        // wAITING
        team_table(true);
        team_message(true, game.current_team.name);
        question_table(false);
        document.getElementById("status").innerHTML = "Status: Warten";
    } else {
        team_table(false);
        team_message(false);
        question_table(true);
        document.getElementById("status").innerHTML = "Status: Sonstiges";
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

    // on-site event handlers
    $("#btn").click(function() {
        //eel.handleinput($("#inp").val());
        $('#inp').val('');
    });

    // onload functionallity
    process_gamestate();
});
