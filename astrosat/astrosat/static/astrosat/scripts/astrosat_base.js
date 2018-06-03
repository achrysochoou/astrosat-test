/* base.js */

/* this project mostly uses Angular for the client */
/* preferably angular-ui-bootstrap */
/* sometimes it uses Bootstrap directly for look-and-feel stuff */
/* but sometimes, when all else fails, it uses pure JQuery or JavaScript */
/* that code is defined here */

/**************************/
/* begin message handling */
/**************************/

function show_msg(text, status) {
    status = typeof status !== 'undefined' ? status : "default";
    var box = bootbox.alert(text);
    box.find(".modal-content").addClass(status);
}

function check_msg() {
    /* gets all pending Django messages */

    var messages_url = "/services/messages/";

    $.ajax({
        url: messages_url,
        type: "GET",
        cache: false,
        success: function (data) {
            $.each(data, function (i, message) {
                show_msg(message.text, message.status);
            });
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText + status + error)
        }
    });
};

/************************/
/* end message handling */
/************************/
