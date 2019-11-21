async function fill_team_table() {
    var tbl = document.getElementById('teamtable');
    let teams = await eel.list_teams()()
    for (var i = 0; i < teams.length; i++) {
        var team = teams[i];
        team.players[0].name

        var row = tbl.insertRow(tbl.rows.length);
        row.insertCell(0).innerHTML = "<input type='button' id='start_team' onclick='eel.start_team("+team.id+")' value='Spielen'>";
        row.insertCell(1).innerHTML = team.id;
        row.insertCell(2).innerHTML = team.name;
    }
}

$(async function() {

    // exposed functions
    eel.expose(dashboard_set_heading);
    function dashboard_set_heading(x) {
        $('#heading').text(x);
    }

    eel.expose(dashboard_set_subheading);
    function dashboard_set_subheading(x) {
        $('#subheading').text(x);
    }

    eel.expose(dashboard_set_url);
    function dashboard_set_url(url) {
        window.location.href = url;
    }

    // on-site event handlers
    $("#btn").click(function() {
        //eel.handleinput($("#inp").val());
        $('#inp').val('');
        eel.random_team()
    });

    // onload functionallity
    let state = await eel.game_state()();
    if (state == 0){
        // PREPARATION
        fill_team_table()
    } else if (state == 1) {

    } else {
    }

});
