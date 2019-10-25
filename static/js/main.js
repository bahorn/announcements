// Parameters
const endDate = new Date(2019, 9, 27, 12, 0).getTime(); //TODO Check this date //remember month is 0-indexed and day is 1-indexed
const displayTime = 5000;

// Global Varibles
const countdown = document.getElementById("countdown");
const overlay = document.getElementById("overlay");
const countClock = document.getElementById("count-clock");
// const realClock = document.getElementById("real-clock");
const announcementTitleDiv = document.getElementById("alert-title");
const announcementBodyDiv = document.getElementById("alert-body");
const audio = document.getElementById('notification');
let displaying = false;
let queue = [];

function updateTime() {
    let dateNow = new Date();

    // COUNTDOWN TIME
    let remainingTime = endDate - dateNow.getTime();
    let hoursLeft = Math.floor((remainingTime % (1000 * 60 * 60 * 24 * 365.25)) / (1000 * 60 * 60));
    let minutesLeft = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
    let secondsLeft = Math.floor((remainingTime % (1000 * 60)) / 1000);

    if (secondsLeft < 10 && minutesLeft != 0) {
        secondsLeft = "0" + secondsLeft;
    }
    if (minutesLeft < 10 && hoursLeft != 0) {
        minutesLeft = "0" + minutesLeft;
    }
    let timeLeft = secondsLeft;
    timeLeft = minutesLeft > 0 ? minutesLeft + ":" + timeLeft : timeLeft;
    timeLeft = hoursLeft > 0 ? hoursLeft + ":" + timeLeft : timeLeft;

    //Above does not account for passing the end date since:
    if (remainingTime < 0) {
        timeLeft = "TIME'S UP!"; //TODO Change the wording here
        countdown.classList.add("time-up");
    }

    countClock.innerText = timeLeft;
    countClock.textContent = timeLeft;

    // setTimeout(updateTime, 1000); // calls showRealTime after 1000 ms
}

function setDisplayTimeOnly() {
    console.log("display time only");
    displaying = false;
    off();
}

function on() {
    console.log("overlay on");
    overlay.style.visibility = "visible";
}

function off() {
    console.log("overlay off");
    overlay.style.visibility = "hidden";
}

function announcement(announcementText) {
    audio.play().then(() => console.log("Playing sound!"));
    // let json = JSON.parse(announcementText);
    let json = announcementText;
    // displays the time remaining in small, and the announcement text
    // AUTOMATICALLY RESETS AFTER TIMEOUT
    displaying = true;
    // set display
    announcementTitleDiv.innerText = json['title'];
    // announcementTitleDiv.textContent = json['title'];
    announcementBodyDiv.innerText = json['body'];
    // announcementBodyDiv.textContent = json['body'];

    on();
    setTimeout(setDisplayTimeOnly, displayTime);

    // create card
    let card = document.createElement('div');
    card.classList.add('card');
    let cardBody = document.createElement('div');
    cardBody.classList.add('card-body');
    card.appendChild(cardBody);

    let title = document.createElement('h2');
    title.classList.add('card-title');
    title.innerText = json['title'];
    cardBody.appendChild(title);

    let time = document.createElement('h6');
    time.classList.add('text-muted', 'card-subtitle', 'mb-2');
    time.innerText = json['time'];
    cardBody.appendChild(time);

    let body = document.createElement('p');
    body.classList.add('card-text', 'h4');
    body.innerText = json['body'];
    cardBody.appendChild(body);

    // insert card into announcement list
    let announcements = document.getElementById('announcements');
    announcements.prepend(card);
}

function loop() {
    // main logic for getting and pushing announcements
    if (displaying === false) {
        console.log("display");
        if (queue.length > 0) {
            const announcementText = queue.shift();
            announcement(announcementText);
        }
    }
    updateTime();
    setTimeout(loop, 1000);
}


$(document).ready(function () {
    //connect to the socket server.
    const pusher = new Pusher('e26d2d5c77e1ace54c55', {
        cluster: 'eu',
        forceTLS: true
    });

    const channel = pusher.subscribe('announcements');
    channel.bind('new', function (data) {
        queue.push(data);
    });

    console.log("Ready");
    //receive details from server
    updateTime(); // the timers are always updated;
    setDisplayTimeOnly(); // always start on default display


    $.getJSON('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=wrussell1999&api_key=eacc77543fa3500e1d9ef91a4b698f80&format=json', function (data) {
        const track = data.recenttracks.track[0];
        $('#lastfm').html(track.artist["#text"] + " - " + track.name)
    });
    overlay.onclick = function () {
        off();
    };

    window.onresize = function () {
        if (window.innerWidth < 750) {
            document.getElementById('snazz').classList.add('flex-column');
            document.getElementById('twitter').classList.add('d-none');
        } else {
            document.getElementById('snazz').classList.remove('flex-column');
            document.getElementById('twitter').classList.remove('d-none');
        }
    };
    window.onresize();
    loop();
});
