function phone_select_player() {
    openFullscreen();
    window.history.replaceState({}, null, 'index.html?player');
    $('#device-chooser').hide();
    $('#player-buttons').show();
}

function phone_select_chaser() {
    openFullscreen();
    window.history.replaceState({}, null, 'index.html?chaser');
    $('#device-chooser').hide();
    $('#chaser-buttons').show();
}

$(async function() {
    url = new URL(window.location.href);

    if (url.searchParams.get('player') != null) {
        phone_select_player();
    } else if (url.searchParams.get('chaser') != null) {
        phone_select_chaser();
    } else {
        $('#device-chooser').show();
        $('#chaser-buttons').hide();
        $('#player-buttons').hide();
    }
});
