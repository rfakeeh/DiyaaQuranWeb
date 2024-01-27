$(document).ready(function () {

    $('#send').on('click', function (event) {

        let prompt_text = $('#text').val();
        let prompt_html = "<div class='row user-prompt'><div class='col-1'><img src='../static/img/user.png' class='user'></div><div class='col prompt'><p class='text'>"+prompt_text+"</p><img class='img'/><p class='video'></p></div></div>";
        let service_url = "/process_text";
        $('#chat-body').append(prompt_html);
        if (isUrl(prompt_text)) {
            let service_url = "/process_video";
        } 

        $.ajax({
            data: {
                text: prompt_text
            },
            type: "POST",
            url: service_url,
        }).done(function (data) {

            if (data.response) {
                console.log(data);
                let response_text = data.response;
                let response_html = "<div class='row diyaa-response'><div class='col-1'><img src='../static/img/logo.png' class='diyaa'></div><div class='col response'><p class='text' id='response'>"+response_text+"</p></div></div>";
                $('#chat-body').append(response_html);

            } else {
                let response_text = "عذرا حصل خطأ غير متوقع يرجي إعادة الارسال ";
                let response_html = "<div class='row diyaa-response'><div class='col-1'><img src='../static/img/logo.png' class='diyaa'></div><div class='col response'><p class='text' id='response'>"+response_text+"</p></div></div>";
                $('#chat-body').append(response_html);

            }
        }).fail(function(jqXHR, textStatus, errorThrown) {            
            let response_text = "عذرا حصل خطأ غير متوقع يرجي إعادة الارسال ";
            let response_html = "<div class='row diyaa-response'><div class='col-1'><img src='../static/img/logo.png' class='diyaa'></div><div class='col response'><p class='text' id='response'>"+response_text+"</p></div></div>";
            $('#chat-body').append(response_html);
        });

    });


});

function redirectToPage(href) {
    window.location.href = href;
}

function isUrl(string) {
    var urlRegex = /^(?:\b(https?|ftp):\/\/)?(?!\.)(?:(?:[a-z\d-]{2,}\.)+(?:[a-z]{2,})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?::\d{2,5})?(?:[\/?#]\S*)?$/i;
    return urlRegex.test(string);
}



