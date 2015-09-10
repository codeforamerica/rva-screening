// Modified from http://www.saltycrane.com/blog/2014/09/bank-style-session-timeout-example-using-jquery-bootstrap-and-flask/
sessionMonitor = function(options) {
    "use strict";

    var defaults = {
        // Session lifetime (milliseconds)
        sessionLifetime: 2 * 60 * 1000,
        // Minimum time between pings to the server (milliseconds)
        minPingInterval: 1 * 60 * 1000,
        // Space-separated list of events passed to $(document).on() that indicate a user is active
        activityEvents: 'mouseup keyup',
        // URL to ping the server using HTTP POST to extend the session
        pingUrl: '/ping',
        // URL to temporarily save any unsaved form data so it can be restored
        unsavedDataUrl: '/unsaved_form',
        // URL used to log out when the session times out
        timeoutUrl: '/relogin',
        ping: function() {
            // Ping the server to extend the session expiration using a POST request.
            $.ajax({
                type: 'POST',
                url: self.pingUrl
            });
        },
        onbeforetimeout: function() {
            // By default this does nothing. Override this method to perform actions
            // (such as saving draft data) before the user is automatically logged out.
            // This may optionally return a jQuery Deferred object, in which case
            // ontimeout will be executed when the deferred is resolved or rejected.
            form_json = JSON.stringify($("#patient_details_form :input")
                .filter(function(index, element) {
                    return $(element).val() != "";
                })
                .serializeArray())

            $.ajax({
                type: 'POST',
                url: self.unsavedDataUrl,
                data: {
                    patient_id: $("#patient_id").val(),
                    form_json: form_json
                }
            });
        },
        ontimeout: function() {
            // Go to the timeout page.
            window.location.href = self.timeoutUrl;
        }
    },
    self = {},
    _expirationTimeoutID,
    // The time of the last ping to the server.
    _lastPingTime = 0;

    function extendsess() {
        // Extend the session expiration. Ping the server and reset the timers if
        // the minimum interval has passed since the last ping.
        var now = $.now(),
            timeSinceLastPing = now - _lastPingTime;

        if (timeSinceLastPing > self.minPingInterval) {
            _lastPingTime = now;
            _resetTimers();
            self.ping();
        }
    }

    function _resetTimers() {
        // Reset the session expiration timer.
        window.clearTimeout(_expirationTimeoutID);
        _expirationTimeoutID = window.setTimeout(_onTimeout, self.sessionLifetime);
    }

    function _onTimeout() {
        // A wrapper that calls onbeforetimeout and ontimeout and supports asynchronous code.
        $.when(self.onbeforetimeout()).always(self.ontimeout);
    }

    // Add default variables and methods, user specified options, and non-overridable
    // public methods to the session monitor instance.
    $.extend(self, defaults, options, {
        extendsess: extendsess
    });
    // Set an event handler to extend the session upon user activity (e.g. mouseup).
    $(document).on(self.activityEvents, extendsess);
    // Start the timers and ping the server to ensure they are in sync with the
    // backend session expiration.
    extendsess();

    return self;
};

// Configure and start the session timeout monitor
sessMon = sessionMonitor({
    // Subtract 30 sends to ensure the backend doesn't expire the session first
    sessionLifetime: (15 * 60 * 1000) - (1 * 30 * 1000),
    minPingInterval: 1 * 60 * 1000,  // 1 minute
    pingUrl: '/ping',
    timeoutUrl: '/relogin',
    // The "mouseup" event was used instead of "click" because some of the
    // inner elements on some pages have click event handlers that stop propagation.
    activityEvents: 'mouseup keyup'
});

window.sessMon = sessMon;
