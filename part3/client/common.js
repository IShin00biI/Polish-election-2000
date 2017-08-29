window.pkw = window.pkw || {};

pkw.setUpErrors = function() {
    $(document).ajaxError(function () {
        alert("An error occurred!");
    });
};

pkw.serverAddr = "http://localhost:8000/pkw/";

pkw.refreshLogStripe = function(logoutCallback, callbackData) {
    var logStripe = $(".logstripe").empty();
    username = localStorage.getItem("pkw_username");
    if(username) {
        logStripe.text(username + " ").append($("<a>").text("Wyloguj").click(function() {
            localStorage.removeItem("pkw_username");
            localStorage.removeItem("pkw_password");
            if(logoutCallback && callbackData)
                logoutCallback(callbackData)
        }));
    }
    else
        logStripe.html('<a href="./login.html">Zaloguj</a>');
};
