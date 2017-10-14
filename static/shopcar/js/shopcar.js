/* 
 *提示登录
 */
$('document').ready(function() {
    getLogin();
})

/* 
 *控制元素物理尺寸
 */
$('.col-xs-1,.col-sm-1').height($('.col-xs-1,.col-sm-1').next().height()+'px');

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
    selectList = $("input.checked:checked").parents('.carlist');
    cal_sum();
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
});
// 数字失去焦点
$('.carlist').on("blur", '.carnum', function() {
           var sum = cal_sum();
           $('.sum_price').text(sum.toFixed(2));
   });
//按键起来事件  验证是否为数字
$('.carlist').on("keydown", '.carnum', function() {
    this.value=this.value.replace(/\D/g,'')
   });


window.onload = function() {
        var selectList = $("input.checked:checked").parents('.carlist');
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
        num = parseFloat($(selectList[i]).find('.carnum').val());
        sum += price * num;
    }
    return sum;
};

/* 
 *加按钮
 */
$('.carlist').on("click", '.addition', function() {
    $(this).siblings('.subtraction').css('color','inherit');
    var quantity = $(this).next().val();
    quantity = parseInt(quantity);
    $(this).next().val(quantity + 1);
    var sum = cal_sum();
    $('.sum_price').text(sum.toFixed(2));
});
/* 
 *减按钮
 */
$('.carlist').on("click", '.subtraction', function() {
    var quantity = $(this).prev().val();
    var quantity = parseInt(quantity);
    if (quantity <=1) {
        $(this).prev().val(0);
        $(this).css('color','#ccc');
    } else {
        $(this).prev().val(quantity - 1);
        var sum = cal_sum();
        $('.sum_price').text(sum.toFixed(2));
    };
});

/* 
 *提交按钮
 */
$('a.menu-right').click(function() {
    if(selectList.length<1){
        $('.menu-right').css({'background-color':'#505050','color':'#eee'});
        $('.menu-right::after').css({'border-color':'#505050!important'})
        return;
    }
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
        product.num = aCarnum.val();
        products.push(product);
    }
    //商品列表数组保存到cookie
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('.sum_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
    window.location.href = '/bill/bills/?new';
})

