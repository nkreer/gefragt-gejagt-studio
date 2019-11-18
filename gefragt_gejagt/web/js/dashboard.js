$(function() {
    eel.expose(dashboard_set_heading); // Expose this function to Python
    function dashboard_set_heading(x) {
        $('#heading').text(x.value);
    }

    eel.expose(dashboard_set_url);

    function dashboard_set_url(url) {
        window.location.href = url;
    }

    $("#btn").click(function() {
        //eel.handleinput($("#inp").val());
        $('#inp').val('');
        eel.list_teams()
    });
});
