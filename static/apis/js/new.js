 
mark = false;
$('.btn-delete').click(function() {
     //loading
    if( mark == true){
        return;
    }
    mark = true; 
     
　
    var id = $(this).attr("id");
    data={}; 
        data['id'] = id; 
        data['method'] = 'delete'; 
        data['csrfmiddlewaretoken']=getCookie('csrftoken');
    
    $.ajax({
        type: 'post',
        url: '/apis/apis/',
        data: data,
        success: function(result) {
            if (result['status'] == 'ok'){
                $().message(result['msg']);  
            } 
            else{
                $().message(result['msg']);  
            }
        },
        error: function() {
            // 500
            alert('server is down!')
            mark = false;
            // unloading
        }
    })
});

