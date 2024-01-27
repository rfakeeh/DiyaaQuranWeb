$(document).ready(function () {

    let image_src = null;

    $('#attach').click(function() {
        $('#image').click();
    });

    // When a file is selected, display the image preview
    $('#image').change(function() {
        if (this.files && this.files[0]) {
            $('#text').val(this.files[0].name);

            var reader = new FileReader();
            reader.onload = function(e) {
                image_src = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $('#send').on('click', function (event) {

        let prompt_text = $('#text').val();
        let prompt_html = "<div class='row user-prompt'><div class='col-1'><img src='../static/img/user.png' class='user'></div><div class='col prompt'><p class='text'>"+prompt_text+"</p></div></div>";
        let service_url = "/process_text";
        let prompt_data = {text: prompt_text};

        if (image_src!=null) {
            service_url = "/process_image";
            prompt_html = "<div class='row user-prompt'><div class='col-1'><img src='../static/img/user.png' class='user'></div><div class='col prompt'><img src='"+image_src+"' width='400'/></div></div>";
            $.ajax({
                data: new FormData($('#form')[0]),
                type: "POST",
                url: service_url,
                cache: false,
                processData: false,
                contentType: false,
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
    
        } else {

            $.ajax({
                data: {
                    text: prompt_text,
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

        }
        
        $('#chat-body').append(prompt_html);
        console.log(service_url);
        image_src = null;
        $('#text').val("");

    });


});

function redirectToPage(href) {
    window.location.href = href;
}

function isUrl(string) {
    var urlRegex = /^(?:\b(https?|ftp):\/\/)?(?!\.)(?:(?:[a-z\d-]{2,}\.)+(?:[a-z]{2,})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?::\d{2,5})?(?:[\/?#]\S*)?$/i;
    return urlRegex.test(string);
}



