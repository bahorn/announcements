// Parameters
const endDate = new Date(2019, 9, 27, 12, 0).getTime(); //TODO Check this date //remember month is 0-indexed and day is 1-indexed
const displayTime = 30000;

// Global Varibles
const countdown = document.getElementById("countdown");
const countClock = document.getElementById("count-clock");
const realClock = document.getElementById("real-clock");
const announcementTitleDiv = document.getElementById("announcement-title");
const announcementBodyDiv = document.getElementById("announcement-body");
const bar = document.getElementById("bar");

let displaying = false;
let queue = []; 

function updateTime(){
	let dateNow = new Date();
	let h = dateNow.getHours(); // 0-23 hours
	let m = dateNow.getMinutes(); // 0-59 - minutes
	let s = dateNow.getSeconds(); // 0-59 - seconds

	// CURRENT TIME
	//time formatting as 2 digits
	h = h > 9 ? h : "0" + h;
	m = m > 9 ? m : "0" + m;
	s = s > 9 ? s : "0" + s;
	time = h + ":" + m + ":" + s;
	realClock.innerText = time; // may not work in Firefox
	realClock.textContent = time; // may not work in IE

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

	setTimeout(updateTime,1000); // calls showRealTime after 1000 ms
}

function setDisplayTimeOnly() {
	displaying = false;

	countdown.classList.add("display-time");
	countdown.classList.remove("announcement");
}

function announcement(announcementText) {	
	countdown.classList.add("announcement");
	countdown.classList.remove("display-time");

	// displays the time remaining in small, and the announcement text
	// AUTOMATICALLY RESETS AFTER TIMEOUT
	displaying = true;
	// set display
	announcementTitleDiv.innerText = announcementText[1];
	announcementTitleDiv.textContent = announcementText[1];
	announcementBodyDiv.innerText = announcementText[2];
	announcementBodyDiv.textContent = announcementText[2];
	
	bar.style.animationDuration = (displayTime / 1000) + "s";

	setTimeout(setDisplayTimeOnly, displayTime);
}

function loop() {
	// main logic for getting and pushing announcements
	if (displaying == false) {
		if (queue.length > 0) {
			const announcementText = queue.shift();
			console.log(announcementText);
			announcement(announcementText);
		}
	}

	setTimeout(loop, 1000);
}

function main() { // the display board logic
	updateTime(); // the timers are always updated;
	setDisplayTimeOnly(); // always start on default display

    let socket = io();
    socket.on('connect', function () {});
    socket.on('announcement', function (data) {
		queue.push(data);
	});

	loop();
}

window.addEventListener('load', main);
