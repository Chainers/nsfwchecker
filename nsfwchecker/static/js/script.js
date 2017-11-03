$(document).ready(function(){
    $("#loader").hide();
    $(".loader-text").hide();
    $(".select-file").click(function(e){
       $('#ff').click();
    });

    $('#ff').on('change', function(e){
        uploadFile();
    });

    $(".checkbtn").click(function(e){
        uploadLink();
    });

    function uploadLink() {
        var url = $('.url').val();
        if (!url)
            return;

        $("#loader").show();
        $(".loader-text").show();
        $('img').attr('src', url);
        $.ajax({
            url: "https://nsfwchecker.com/api/nsfw_url_recognizer",
            type: "POST",
            data: {'url': url},
            success: function(response) {
                    var value = parseFloat(response.nsfw_rate)
                    var rate = Number((value).toFixed(2));
                    $("#loader").hide();
                    $(".loader-text").hide();
                    $("#rate").text("Your nsfw rate: " + rate * 100 + "%");
            },
            error: function(jqXHR, textStatus, errorMessage) {
                console.log(errorMessage); // Optional
            }
        });
    }

    function uploadFile() {
        $("#loader").show();
        $(".loader-text").show();
        var blobFile = ($("#ff"))[0].files[0];
        if (blobFile) {
            var reader = new FileReader();

            reader.onload = function(e) {
                $('img').attr('src', e.target.result);
            }

            reader.readAsDataURL(blobFile);
        }

        var formData = new FormData();
        formData.append("image", blobFile);
        $.ajax({
        url: "https://nsfwchecker.com/api/nsfw_recognizer",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
                var value = parseFloat(response.nsfw_rate)
                var rate = Number((value).toFixed(2));
                $("#loader").hide();
                $(".loader-text").hide();
                $("#rate").text("Your nsfw rate: " + rate * 100 + "%");
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        }
        });
    }
});
