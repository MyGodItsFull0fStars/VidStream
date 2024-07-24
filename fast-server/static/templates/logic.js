const lightDarkModeCookieName = "light-dark-mode";
const lightMode = "light-mode";
const darkMode = "dark-mode";

function getCookie(cookieName) {
    let name = cookieName + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');

    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];

        // consume blank characters
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }

        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }

    return "";
}


function setCookie(cookieName, cookieValue) {
    document.cookie = cookieName + "=" + cookieValue + ";path=/";
}


function playVideo(video) {
    const videoPlayer = document.getElementById('video-player');
    const videoSource = document.getElementById('video-source');

    if (videoPlayer == null || videoSource == null) {
        return
    }

    videoSource.src = video;
    videoPlayer.style.display = 'block';

    videoPlayer.load();
    videoPlayer.play();
}


function checkboxSwitchLever(doc, isChecked) {
    if (isChecked) {
        doc.getElementById('mode-switch').checked = true;
        doc.body.classList.remove(lightMode);
        doc.body.classList.add(darkMode);
        setCookie(lightDarkModeCookieName, darkMode);
    } else {
        doc.getElementById('mode-switch').checked = false;
        doc.body.classList.remove(darkMode);
        doc.body.classList.add(lightMode);
        setCookie(lightDarkModeCookieName, lightMode);
    }
}