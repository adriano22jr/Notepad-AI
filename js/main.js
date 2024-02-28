$(document).ready(function(){
    $("#account-delete-button").click(function(){
        let given_email = $("#email-delete").val();
        $.ajax({
            type: "POST",
            url: "/delete-account",
            data: {"email": given_email},
            statusCode: {
                200: function(){
                    alert("response 200");
                    location.href="{{ url_for('index') }}";
                },
                400: function(){
                    alert("response 400");
                    $("#email-error-alert").css({"display": "block"});
                }
            }
        });
    })
});