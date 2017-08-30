$(document).ready(function() {
    var requestAddr = pkw.serverAddr + "login/";

    pkw.setUpErrors();

    pkw.refreshLogStripe(null, null, true);

    $("#login_button").click(function() {
        var username = $("#username").val();
        var password = $("#password").val();

        if(!username || !password) {
            alert("Wypełnij oba pola!");
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
                    alert("Podano nieprawidłowe dane!");
            });
    });
});
