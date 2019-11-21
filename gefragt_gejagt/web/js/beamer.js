$(async function() {
    // exposed functions
    eel.expose(beamer_set_subheading);
    function beamer_set_subheading(x) {
        $('#subheading').text(x);
    }

    eel.expose(beamer_set_url);
    function beamer_set_url(url) {
        window.location.href = url;
    }
});
