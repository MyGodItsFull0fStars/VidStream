
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
    // document.cookie = cookieName + "=" + cookieValue + ";path=/";
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


// <script>
// window.addEventListener("blur", () => {
//   document.title = "Come Back :("
// })
// window.addEventListener("focus", () => {
//   document.title = "Video Library"
// })

// let lightDarkModeCookieName = "light-dark-mode";
// let cookieValue = getCookie(lightDarkModeCookieName);
// const light = "light";
// const dark = "dark";

// if (cookieValue.length > 0) {
//   if (cookieValue == dark) {
//     modeSwitch.checked = true;
//     document.body.classList.remove('light-mode');
//     document.body.classList.add('dark-mode');
//   } else {
//     this.checked = false;
//     document.body.classList.remove('dark-mode');
//     document.body.classList.add('light-mode');
//   }
// } else {
//   // light mode is the default
//   this.checked = false;
//   document.body.classList.remove('dark-mode');
//   document.body.classList.add('light-mode');
//   setCookie(lightDarkModeCookieName, light);
// }


// document.getElementById('mode-switch').addEventListener('change', function () {
//   if (this.checked) {
//     document.body.classList.remove('light-mode');
//     document.body.classList.add('dark-mode');
//     setCookie(lightDarkModeCookieName, dark);
//   } else {
//     document.body.classList.remove('dark-mode');
//     document.body.classList.add('light-mode');
//     setCookie(lightDarkModeCookieName, light);
//   }
//   alert("WTF????")
// });
// </script>