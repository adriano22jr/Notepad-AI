$(document).ready(function(){
    $("#account-delete-button").click(function(){
        let given_email = $("#email-delete").val();
        $.ajax({
            type: "POST",
            url: "/delete-account",
            data: {"email": given_email},
            statusCode: {
                200: function(){
                    location.href="{{ url_for('index') }}";
                },
                400: function(){
                    $("#email-error-alert").css({"display": "block"});
                }
            }
        });
    })
});

$(document).ready(function(){
    $("#delete-notebook").click(function(){
        let notebook_id = $("#notebook-id").val();
        $.ajax({
            type: "POST",
            url: "/delete-notebook",
            data: {"notebook_id": notebook_id}
        });
    });
});

$(document).ready(function(){
    $("#create-notebook-button").click(function(){
        let notebook_type = $(".form-check input:radio:checked").val();
        let notebook_name = $("#notebookName").val();

        $.ajax({
            type: "POST",
            url: "/redirect-notebook",
            data: {"notebook_type": notebook_type, "notebook_name": notebook_name}
        });
    });
});

$(document).ready(function(){
    $("#edit-button").click(function(){
        $("#note-title").attr("contentEditable", true);
        $("#note-title").css({"border": "1px solid lightgray"});
        $("#edit-button").css({"display": "none"});
        $("#confirm-button").css({"display": "inline-block"});
    });

    $("#confirm-button").click(function(){
        $("#note-title").attr("contentEditable", false);
        $("#note-title").css({"border": "none"});
        $("#edit-button").css({"display": "inline-block"});
        $("#confirm-button").css({"display": "none"});
    });

    $("#edit-content-button").click(function(){
        $("#note-content").attr("contentEditable", true);
        $("#left-div").attr("contentEditable", true);

        $("#note-content").css({"border": "1px solid lightgray"});
        $("#toolbar").css({"display": "block"});
        $("#edit-content-button").css({"display": "none"});
        $("#confirm-content-button").css({"display": "inline-block"});
    });

    $("#confirm-content-button").click(function(){
        $("#note-content").attr("contentEditable", false);
        $("#left-div").attr("contentEditable", false);
        
        $("#note-content").css({"border": "none"});
        $("#toolbar").css({"display": "none"});
        $("#edit-content-button").css({"display": "inline-block"});
        $("#confirm-content-button").css({"display": "none"});
    });
});