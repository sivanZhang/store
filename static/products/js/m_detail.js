/* 选中规格效果
--------------------------*/
$('table.table').on('click', '.rule_tr', function () {
    $(this).siblings().removeClass('act_box');
    $(this).addClass('act_box');
    $('.table').find('.red_msg').remove();
    $('.stock_copy').text($(this).children('.stock').text());
    $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});


/* 加 
--------------------------*/
$('.btn-group').on("click", '.addition', function () {
    var quantity = parseInt($(this).next().text());
    var nStock = parseInt($('.stock_copy').text());
    if (quantity >= nStock) {
        $(this).next().text(nStock)
    } else { $(this).next().text(quantity + 1); }
    //价格变动
     $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});

/* 减去 
--------------------------*/
$('.btn-group').on("click", '.subtraction', function () {
    var quantity = parseInt($(this).prev().text());
    if (quantity <= 1) {
        $(this).prev().text(1);
    } else {
        $(this).prev().text(quantity - 1);
    }
    //价格变动
    $('#total_price').text($('.act_box').children('.unit-price').text() * $('.carnum').text());
});

/* 元素尺寸样式
--------------------------*/
$('.ware_img').height($('.ware_img').width() + 'px');
$('.img_parent').height($('.img_parent').width() + 'px');
$('.number').height($('.img_parent').height() + 'px');
$('.number div').height($('.number').height() / 3 + 'px');
$('.number div').css('line-height', $('.number div').height() + 'px');
$('#swiper-container').height($('#swiper-container').width() + 'px');
$('.illustrate img').attr('height','auto');
$('.illustrate img').attr('width','100%');

/* 商品类型动画 
--------------------------*/
function fnRuleShow(){
    $(".hide_box_wrap").fadeIn();
    $('.hide_box_content').animate({ bottom: '0%' }, 400);
    $('.thumbnail').height($('.thumbnail').width() + 'px');
};
$(".choose").click(function(){
    fnRuleShow();
});
   
$(".hide_box_void,.fa-times").click(function () {
    $('.hide_box_content').animate({ bottom: '-100%' }, 400);
    $(".hide_box_wrap").fadeOut();
});

/* 产品型号页"确定"事件绑定
--------------------------*/
$('.btn-danger-confirm').click(function () {
    getLogin();
    var mark = true;//标记是否全部选中，默认全部选中

    if ($('.table').find('.act_box').length == 0) {
        $('.table').find('.red_msg').remove();
        $('.table').append('<p class="red_msg">请选择</p>');
        mark = false;

    } else {
        $(this).find('.red_msg').remove();
        ajaxSubmit()
    };

    if (mark == true) {
        //选中的业务逻辑
        $('.hide_box_content').animate({ bottom: '-100%' }, 400);
        $(".hide_box_wrap").fadeOut();
    }
});

/* ajax  镶嵌评价页
--------------------------*/
var productid=$('#productid').val();
$(document).ready(function(){
    $.get("/comment/comment/?id="+productid, {}, function(result){
        $('#com_wrap').append(result);
    })
});
/* $('#com_wrap').on('click','.publish',function(){
    $.get('/comment/comment/?id=1', {}, function(result){
        $('#com_wrap').remove(result);
        $('#com_wrap').append(result);
    })错的
})
 */
/*“加入购物车”按钮绑定事件*
--------------------------*/
$('.add-cart').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        fnRuleShow();
    } else {
        ajaxSubmit();
    }
});

/*加入购物车提交程序封装
--------------------------*/
function ajaxSubmit() {
    var url = '/shopcar/shopcars/';
    var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

    var ruleid = $('.act_box').attr('ruleid')
    var quantity = parseInt($('#carnum').text());
    var data = {
        'method': 'create',
        'ruleid': ruleid,
        'num': quantity,
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    $.ajax({
        url: url,
        type: 'post',
        data: data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $().message(result['msg']);
            }
            else {
                $().message(result['msg']);
            }
        },
        error: function () { // 500
            $().errormessage('server is down!');
        }
    });
}

/* ajax  立即购买*
--------------------------*/
$('.buy-now').click(function () {
    getLogin();
    if ($('.act_box').length === 0) {
        $('.table').find('.red_msg').remove();
        $('.table').append('<p class="red_msg">请选择</p>');
    } else {
        var url = '/shopcar/shopcars/';
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    
        var ruleid = $('.act_box').attr('ruleid')
        var quantity = parseInt($('#carnum').text());
        var data = {
            'method': 'create',
            'ruleid': ruleid,
            'num': quantity,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
        $.ajax({
            url: url,
            type: 'post',
            data: data,
            success: function (result) {
                if (result['status'] == 'ok') {
                    $().message(result['msg']);
                    productCookie();
                    window.location.href = '/bill/bills/?new';
                }
                else {
                    $().message(result['msg']);
                }
            },
            error: function () { // 500
                $().errormessage('server is down!');
            }
        });
    }
});


/* 商品信息存入COOKIE */
function productCookie(){
    var products = new Array();
    var product = {};
        product.name = $('.item_name').text();
        product.rule = $('.rule_name').text();
        product.img = $('.hide_box_content .thumbnail').attr('src');
        product.Price = $('.unit-price').text();
        product.ruleid = $('.rule_tr').attr('ruleid');
        product.num = $('#carnum').text();
        products.push(product);
    
    products = JSON.stringify(products);
    CookieUtil.set("products", products, '', "/");
    //cookie保存总价
    var sum_price = $('#total_price').text();
    CookieUtil.set("sum_price", sum_price, '', "/");
};
//bootstrap标签页
$('#myTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  });
  var total_price=$('#total_price').text()-0;
  $('#total_price').text(total_price.toFixed(2));
  var comReload=$('#com_wrap');
  $('#com_wrap').on('click','.publish',function(){
    window.location.reload();
  })

  var mySwiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    prevButton: '.swiper-button-prev',
    nextButton: '.swiper-button-next',
    autoplay: 3000,
    speed: 300,
});