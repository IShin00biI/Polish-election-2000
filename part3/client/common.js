window.pkw = window.pkw || {};

pkw.serverAddr = "http://localhost:8000/pkw/";

pkw.setUpErrors = function() {
    $(document).ajaxError(function (event, jqxhr, settings, thrownError) {
        alert("Wystąpił błąd w komunikacji z serwerem!" +
            "\nKod: " + jqxhr.status +
            "\nBłąd: " + thrownError);
    });
};

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
