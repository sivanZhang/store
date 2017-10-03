//  发表+存稿按钮    >>> 点击事件
$('.product-btn').click(function() {
    var categoryid = $('#sel-category').val();
    var title = $('#title').val();
    var desc = $('#desc').val();

    var detail = tinymce.get("detail").getContent();
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
  
    

    data = {
        'method': 'create',
        'categoryid': categoryid,
        'title': title,
        'description': desc,
        'detail': detail,
        'rules': JSON.stringify(rules),
        'parameters': JSON.stringify(parameters),
        'status': $(this).attr('status'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    var product = $('#productid');
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }

    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function(result) {
            $('.msg').append(html.replace('###', result['msg']));
        },
        error: function() {
            // 500
            alert('server is down!')
        }
    })
});
