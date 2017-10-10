//  提交订单
$('.submit-btn-test').click(function() { 
    var address_id = 1;
    var phone = '18811082245';
    var reciever = '张继伟'
    var products = Array();
    product ={
        'ruleid': 3,
        'num': 7
    }
    products.push(item);
    product ={
        'ruleid': 4,
        'num': 7
    }
    products.push(item);
    data = {
        'method': 'create',
        'address_id': address_id,
        'phone': phone,
        'reciever': reciever,
        'items': JSON.stringify(products),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
   

    $.ajax({
        type: 'post',
        url: '/bill/bills/',
        data: data,
        success: function(result) {
            $().message(result['msg']); 
        },
        error: function() {
            // 500
            alert('server is down!')
        }
    })
}); 