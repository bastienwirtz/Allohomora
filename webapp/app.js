(function() {
    'use strict';

    var socket = io.connect('http://192.168.0.112:5000');

    // Notification initialization
    var nativeNotification = false;
    if (window.Notification && Notification.permission === "default") {
        Notification.requestPermission(function (permission) {
            nativeNotification = (permission === "granted");
        });
    } else if (window.Notification && Notification.permission === "granted") {
        nativeNotification = true;
    }

    var app = new Vue({
        el: '#app',
        data: {
            events: []
        },
        created: function() {
            socket.on('opened', function(event) {
                console.log(event);
                this.events.push({
                    date: new Date().toLocaleDateString(),
                    hour: new Date().toLocaleTimeString(),
                    source: event.source,
                });
                this.notify('Door opened');
            }.bind(this));
            socket.on('ringing', function(event) {
                console.log(event);
                this.notify('Someone knocking at the door!');
            }.bind(this));
        },
        methods: {
            openDoor: function () {
                this.$http.get('http://192.168.0.112:5000/open').then((response) => {
                    console.log('Door open successfully');
                }, (response) => {
                    this.notify('An error occurred');
                });

            },
            notify: function (message) {
                if (nativeNotification) {
                    new Notification(message);
                } else {
                    var notification = document.querySelector('.mdl-js-snackbar');
                    notification.MaterialSnackbar.showSnackbar({message: message});
                }
            }
        }
    });

})();