// exposed functions
eel.expose(all_set_url);
function all_set_url(url) {
    window.location.href = url;
}

function set_modal(status, id) {
    modal = document.getElementById(id);
    if (status) {
        modal.classList.add('is-active');
        document.documentElement.classList.add('is-clipped');
    } else {
        modal.classList.remove('is-active');
        document.documentElement.classList.remove('is-clipped');
    }
}
