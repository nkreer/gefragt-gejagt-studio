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

/* Get the documentElement (<html>) to display the page in fullscreen */
var elem = document.documentElement;

/* View in fullscreen */
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
    }
}
