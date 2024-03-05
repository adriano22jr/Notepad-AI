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
        
        $("#note-content").css({"border": "1px solid lightgray"});
        $("#toolbar").css({"display": "block"});
        $("#edit-content-button").css({"display": "none"});
        $("#confirm-content-button").css({"display": "inline-block"});
    });

    $("#confirm-content-button").click(function(){
        $("#note-content").attr("contentEditable", false);
        
        $("#note-content").css({"border": "none"});
        $("#toolbar").css({"display": "none"});
        
        $("#savedb-button").css({"display": "inline-block"});
        $("#edit-content-button").css({"display": "inline-block"});
        $("#confirm-content-button").css({"display": "none"});
    });

    $("edit-markdown-content-button").click(function(){
        $("#left-div").attr("contentEditable", true);

        $("#edit-markdown-content-button").css({"display": "none"});
        $("#confirm-markdown-content-button").css({"display": "inline-block"});
    });

    $("confirm-markdown-content-button").click(function(){
        $("#left-div").attr("contentEditable", false);

        $("savedb-markdown-button").css({"display": "inline-block"});
        $("#edit-markdown-content-button").css({"display": "inline-block"});
        $("#confirm-markdown-content-button").css({"display": "none"});
    });
});