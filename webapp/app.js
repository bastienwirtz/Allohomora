(function() {
    'use strict';
    var app5 = new Vue({
        el: '#app',
        data: {
            events: [{
                date: new Date().toLocaleDateString(),
                hour: new Date().toLocaleTimeString(),
                source: 'Web',
            }]
        },
        methods: {
            openDoor: function () {
                this.$http.get('http://192.168.0.112:5000/open').then((response) => {
                    this.events.push({
                        date: new Date().toLocaleDateString(),
                        hour: new Date().toLocaleTimeString(),
                        source: 'Web',
                    });
                }, (response) => {
                    var notification = document.querySelector('.mdl-js-snackbar');
                    notification.MaterialSnackbar.showSnackbar(
                          {
                            message: 'An error occurred'
                          }
                    );
                });

            }
        }
    })
})();