// Parameters
var endDate = new Date(2019, 9, 27, 12, 0).getTime(); //TODO Check this date //remember month is 0-indexed and day is 1-indexed
var displayTime = 30000;
var alertBackgroundColor = "#f15a22";
var normalBackgroundColor = "#2f3c63";
var alertForegroundColor = "black";
var normalForegroundColor = "white";

// Global Varibles
var countClock = document.getElementById("count-clock");
var realClock = document.getElementById("real-clock");
var announcementDiv = document.getElementById("announcement");
var bar = document.getElementById("bar");
var displaying = false;
var queue = []; 

function updateTime(){
	var dateNow = new Date();
	var h = dateNow.getHours(); // 0-23 hours
	var m = dateNow.getMinutes(); // 0-59 - minutes
	var s = dateNow.getSeconds(); // 0-59 - seconds

	// CURRENT TIME
	//time formatting as 2 digits
	h = h > 9 ? h : "0" + h;
	m = m > 9 ? m : "0" + m;
	s = s > 9 ? s : "0" + s;
	time = h + ":" + m + ":" + s;
	realClock.innerText = time; // may not work in Firefox
	realClock.textContent = time; // may not work in IE

	// COUNTDOWN TIME
	var remainingTime = endDate - dateNow.getTime();
	var hoursLeft = Math.floor((remainingTime % (1000 * 60 * 60 * 24 * 365.25)) / (1000 * 60 * 60));
  	var minutesLeft = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
  	var secondsLeft = Math.floor((remainingTime % (1000 * 60)) / 1000);
  	
  	if (secondsLeft < 10 && minutesLeft != 0) {
  		secondsLeft = "0" + secondsLeft;
  	}
  	if (minutesLeft < 10 && hoursLeft != 0) {
 		minutesLeft = "0" + minutesLeft;
   	}
   	var timeLeft = secondsLeft;
   	timeLeft = minutesLeft > 0 ? minutesLeft + ":" + timeLeft : timeLeft;
   	timeLeft = hoursLeft > 0 ? hoursLeft + ":" + timeLeft : timeLeft;

   	//Above does not account for passing the end date since:
   	if (remainingTime < 0) {
   		timeLeft = "TIME'S UP!"; //TODO Change the wording here
   		countClock.style.fontSize = "10em";
   	}

  	countClock.innerText = timeLeft;
  	countClock.textContent = timeLeft;

	setTimeout(updateTime,1000); // calls showRealTime after 1000 ms
}

function setDisplayTimeOnly() {
	displaying = false;

	// displays only the countdown clock and the real time clock, sets any announcement to empty string 
	countClock.style.display = "block";
	realClock.style.display = "block";
	announcementDiv.style.display = "none";
	announcementDiv.innerText = "";
	announcementDiv.textContent = "";
	bar.style.display = "none";

	//resets the size style of the clocks
	countClock.style.margin = "7vh auto 0px auto";
	countClock.style.fontSize = "15em";
	realClock.style.margin = "0px auto"; 
	realClock.style.fontSize = "3em";

	//reset page style
	document.body.style.background = normalBackgroundColor;
	document.body.style.color = normalForegroundColor;
}

function announcement(announcementText) {	
	// displays the time remaining in small, and the announcement text
	// AUTOMATICALLY RESETS AFTER TIMEOUT
	displaying = true;
	// set display
	countClock.style.display = "block";
	realClock.style.display = "none";
	announcementDiv.style.display = "block";
	announcementDiv.innerText = announcementText;
	announcementDiv.textContent = announcementText;
	
	bar.style.animationDuration = (displayTime / 1000) + "s";
	bar.style.backgroundColor = alertForegroundColor;
	bar.style.display = "block";

	// styles
	countClock.style.margin = "7vh auto 0px auto";
	countClock.style.fontSize = "5em";

	// alert colour
	document.body.style.background = alertBackgroundColor;
	document.body.style.color = alertForegroundColor;

	setTimeout(setDisplayTimeOnly, displayTime);
}

function loop() {
	// main logic for getting and pushing announcements
	if (displaying == false) {
		if (queue.length > 0) {
			var announcementText = queue.shift();
			console.log(announcementText);
			announcement(announcementText);
		}
	}

	setTimeout(loop, 1000);
}

function main() { // the display board logic
	updateTime(); // the timers are always updated;
	setDisplayTimeOnly(); // always start on default display

    var socket = io();
    socket.on('connect', function () {});
    socket.on('announcement', function (data) {
		queue.push(data);
	});

	loop();
}

window.addEventListener('load', main);
