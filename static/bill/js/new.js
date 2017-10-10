/* 
 *获取cookid数据
 */
var nSum_price =JSON.parse(CookieUtil.get("sum_price"));//总价格
var aProducts=JSON.parse(CookieUtil.get("products"));//商品
var oAdress= JSON.parse(CookieUtil.get("aAddress"));//快递地址

/* 
 *显示总价
 */
$('#sum_price').text(nSum_price);
/* 
 *显示总件数
 *图片显示
 */
var sum_number=0;
var oImg=  $('img.thumbnail')
for (var i = 0; i < aProducts.length; i++) {
  sum_number += parseInt(aProducts[i].num);
  //图片显示
  var aSrc=aProducts[i].img;
  $(oImg[i]).attr('src',aSrc)
};
$('#sum_number').text('共'+sum_number+'件');

/* 
 *地址栏text
 */
$('#name').text('姓名：'+oAdress.name);
$('#phone').text('电话：'+oAdress.phone);
var addressIcon = '<i class="fa fa-map-marker" aria-hidden="true"></i>:';
$('#address').html(' <div id="address">'+addressIcon+oAdress.address+'</div>');


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
   
  
    
    var address_id = 1;
    var phone = '18811082245';
    var reciever = '张继伟'*/
    var items = Array();
    for (var i = 0; i < aProducts.length; i++) {
        item ={
            'ruleid':aProducts[i].ruleid,
            'num':aProducts[i].num
        }
        items.push(item);
      };
    data = {
        'method': 'create',
        'address_id': oAdress.address_id,
        'phone': oAdress.phone,
        'reciever': '大哥',
        'items': JSON.stringify(items),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
  /*   var product = $('#productid');
    if (product.length > 0){
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }
    */
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

