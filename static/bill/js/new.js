//  提交订单
$('.submit-btn').click(function() {
    /*
    var categoryid = $('#sel-category').val();
    var title = $('#title').val();
    var desc = $('#desc').val();
    var categoryid = $('#sel-category').val();

    var obj = {};
    var rules = Array();

    var rules_tr = $('.tr_rule');
    rules_tr.each(function() {
        obj['name'] = $(this).find('.name').text();
        obj['unit'] = $(this).find('.type').text();
        obj['price'] = $(this).find('.price').text();
        obj['inv'] = $(this).find('.inv').text();
        rules.push(obj);
        obj = {};
    });
    var parameters = Array();
    var parameters_tr = $('.parameter_tr');
    var obj_para = {};
    parameters_tr.each(function() {
        obj_para['key'] = $(this).find('.key').text();
        obj_para['value'] = $(this).find('.value').text(); 
        parameters.push(obj_para);
        obj_para = {};
    });
    */
  
    
    var address_id = 1;
    var phone = '18811082245';
    var reciever = '张继伟'
    var items = Array();

    data = {
        'method': 'create',
        'address_id': address_id,
        'phone': phone,
        'reciever': reciever,
        'items': JSON.stringify(items),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    var product = $('#productid');
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }

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
