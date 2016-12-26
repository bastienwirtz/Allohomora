(function() {
    'use strict';

    var doorbellUrl = 'http://192.168.1.214:5000';
    var socket = io.connect(doorbellUrl);
    var openDuration = 2500;

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
                var eventTime = new Date(event.time);
                this.events.unshift({
                    label: 'Ouverture',
                    type: 'open',
                    date: eventTime.toLocaleDateString(),
                    hour: eventTime.toLocaleTimeString(),
                    source: event.source,
                });

                $('#btn-open').addClass('disable');

                var bar = new ProgressBar.Circle('#btn-open', {
                    strokeWidth: 6,
                    easing: 'easeInOut',
                    duration: openDuration,
                    color: '#f44336',
                    trailColor: 'transparent',
                    trailWidth: 1,
                    svgStyle: null
                });

                bar.animate(1.0, function() {
                    $('#btn-open').removeClass('disable');
                    bar.destroy();
                });

                this.notify('Door opened');
            }.bind(this));
            socket.on('ringing', function(event) {
                var eventTime = new Date();
                this.events.unshift({
                    label: 'Drinnng',
                    type: 'ring',
                    date: eventTime.toLocaleDateString(),
                    hour: eventTime.toLocaleTimeString(),
                });
                this.notify('Someone knocking at the door!');
            }.bind(this));
        },
        methods: {
            openDoor: function (e) {
                var button = $(e.target).is('a') ? $(e.target) : $(e.target).parent();
                console.log(button);
                if (!button.hasClass('disable')) {
                    this.$http.get(doorbellUrl+'/open').catch(function response() {
                        this.notify('An error occurred');
                    });
                }
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