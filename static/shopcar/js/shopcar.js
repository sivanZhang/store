/* 
 *提示登录
 */
$('document').ready(function() {
    getLogin();
})

/* 
 *控制元素物理尺寸
 */
$('.ware_img').height($('.ware_img').width() + 'px');
$('.img_parent').height($('.img_parent').width() + 'px');
$('.number').height($('.img_parent').height() + 'px');
$('.number div').height($('.number').height() / 3 + 'px');
$('.number div').css('line-height', $('.number div').height() + 'px');

/* 
 *点击复选框更新价格
 */

//全选

$("#all_checked").click(function() {
    if (this.checked) {
        $("input.checked").prop("checked", true);
    } else {
        $("input.checked").prop("checked", false);
    }
});

var selectList = '';
$('body').on("click", "input[type='checkbox']", function() {
    selectList = $("input.checked:checked").parent().parent();
    cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
});
window.onload = function() {
        var selectList = $("input.checked:checked").parent().parent();
        cal_sum();
        var sum = cal_sum();
        $('.sum_price').text(sum.toFixed(2));
    }
    /* 
     *单价x数量的总价格
     */
function cal_sum() {
    var num = 0;
    var sum = 0; //tatol money
    for (var i = 0; i < selectList.length; i++) {
        price = parseFloat($(selectList[i]).find('.carprice').text());
        num = parseFloat($(selectList[i]).find('.carnum').text());
        sum += price * num;
    }
    return sum;
};

/* 
 *加按钮
 */
$('.number').on("click", '.addition', function() {
    var quantity = $(this).next().text();
    quantity = parseInt(quantity);
    $(this).next().text(quantity + 1);
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
});
/* 
 *减按钮
 */
$('.number').on("click", '.subtraction', function() {
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
/* 
 *提交按钮
 */
$('a.menu-right').click(function() {
    //创建商品列表数组，每个元素是一个商品对象
    var products = new Array();
    for (var i = 0; i < selectList.length; i++) {
        var aName = $(selectList[i]).find('.carlist_name'),
            aRule = $(selectList[i]).find('.rule_content'),
            aImg = $(selectList[i]).find('img'),
            aPrice = $(selectList[i]).find('.carprice'),
            aCarnum = $(selectList[i]).find('.carnum'),
            product = {};
        product.name = aName.text();
        product.rule = aRule.text();
        product.img = aImg.attr('src');
        product.Price = aPrice.text();
        product.ruleid = $(aCarnum).attr('ruleid');
        product.num = aCarnum.text();;
        products.push(product);
    }
    //商品列表数组保存到cookie
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('.sum_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
    window.location.href = '/bill/bills/';
})