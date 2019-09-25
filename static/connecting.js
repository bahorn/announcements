window.addEventListener('load', () => {
    var socket = io();
    socket.on('connect', function () {
        console.log("connected");
    });
    socket.on('announcement', function (data) {
        console.log("announcement: " + data);
    });
});