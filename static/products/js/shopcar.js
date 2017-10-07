/*提示登录*/

$('document').ready(function () {
    getLogin();
})


$('.ware_img').height($('.ware_img').width() + 'px');
$('.img_parent').height($('.img_parent').width() + 'px');
$('.number').height($('.img_parent').height() + 'px');
$('.number div').height($('.number').height() / 3 + 'px');
$('.number div').css('line-height', $('.number div').height() + 'px');

var x='';
 $("input[type='checkbox']").bind("click", function () {
    x= $("input[type='checkbox']:checked").parent().parent();
    cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
 }); 
/* 增减商品个数 计算总价格*/
function cal_sum() {
    var num = 0;
    var sum = 0; //tatol money

    for (var i = 0; i < x.length; i++) {
        price = parseFloat($(x[i]).find('.carprice').text());
        num = parseFloat($(x[i]).find('.carnum').text());
        sum += price * num;
    }

    return sum;
};
//加
$('.number').on("click", '.addition', function () {
    var quantity = $(this).next().text();
    quantity = parseInt(quantity);
    $(this).next().text(quantity + 1);
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
});
/* x.find($('.number')) */
//减

$('.number').on("click", '.subtraction', function () {
    var quantity = $(this).prev().text() - 0;
    var quantity = parseInt(quantity);
    if (quantity < 1) {
        $(this).prev().text('0');
    } else {
        $(this).prev().text(quantity - 1);
        var sum = cal_sum();
        $('.sum_price').text(sum.toFixed(2));
    };
});
