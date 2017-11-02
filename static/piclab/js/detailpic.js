$(document).ready(function() {
    $('.btn-upload').click(function() {
      
        
        var formData = new FormData(document.querySelector("#csrftocken_form"));
        formData.append('detailpic', ''); 
        $.ajax('/pic/pics/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data['status'] == 'OK') {
                    $().message(data['msg']);
                    setTimeout(function() {
                        location.reload();
                    }, 3000);
                } else {
                    $().errormessage(data['msg']);
                }
            },
            error: function() {
                $().errormessage('server side error');
            }
        });
    });
     $('.detail-img').height($('.detail-img').width()+'px');
});