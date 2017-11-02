$(document).ready(function(){
 $("#loader").hide();
   $("#jj").click(function(){
        uploadFile();
    });

    function uploadFile() {
    $("#loader").show();
    var blobFile = ($("#ff"))[0].files[0]

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
            $("#rate").text("Your nsfw rate: " + rate * 100 + "%");
       },
       error: function(jqXHR, textStatus, errorMessage) {
           console.log(errorMessage); // Optional
       }
    });
}
});
