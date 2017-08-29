$(document).ready(function() {
    var requestAddr = pkw.serverAddr + "login/";

    pkw.setUpErrors();

    pkw.refreshLogStripe();

    $("#login_button").click(function() {
        var username = $("#username").val();
        var password = $("#password").val();

        if(!username || !password) {
            $(".errormsg").text("Wypełnij oba pola!").show();
            return;
        }

        $.post(requestAddr, {
                username: username,
                password: password
            },
            function(data, status) {
                if(data === "OK") {
                    localStorage.setItem('pkw_username', username);
                    localStorage.setItem('pkw_password', password);
                    window.open("./area.html","_self")
                }
                else
                    $(".errormsg").text("Podano nieprawidłowe dane logowania!").show();
            });
    });
});
