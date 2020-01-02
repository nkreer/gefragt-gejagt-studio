// exposed functions
eel.expose(all_set_url);
function all_set_url(url) {
    window.location.href = url;
}
eel.expose(request_clients_ping);
function request_clients_ping() {
    var id=eel._guid;
    var type=location.pathname.substr(1,location.pathname.indexOf('/',1)-1)
    eel.client_ping({id:id,type:type})
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

offlineDetected = false;
eelReconnectionIntervall = setInterval(() => {
    if (!offlineDetected) {
        if (eel._websocket.readyState >= 2) {
            offlineDetected = true;
            if (!location.href.includes('/beamer')) {
                warning = document.createElement('div');
                warning.innerHTML = '<div id="connectionWarning" style="z-index: 100;position: absolute;top: 0;left: 0;width: 100%;background: #ffdd57;padding: 2rem;"><h2 style="font-weight: bold;">Achtung: Keine Verbingung</h2><span>Sobald der Server wieder online ist, wird sich neu verbunden.</span></div>';
                document.body.appendChild(warning);
            }
            eelServerCheckIntervall = setInterval(() => {
                window.fetch('/available.txt').then((text) => {
                    clearInterval(eelServerCheckIntervall);
                    location.reload(true);
                })
            }, 5000);
        }
    }
}, 1000)
