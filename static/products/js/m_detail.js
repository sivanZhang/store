/* 选中规格效果
--------------------------*/
$('table.table').on('click', '.rule_tr', function () {
    $(this).siblings().removeClass('act_box');
    $(this).addClass('act_box');
    $('.table').find('.red').remove();
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


$('.ware_img').height($('.ware_img').width() + 'px');
$('.ware_img').height($('.ware_img').width() + 'px');
$('.img_parent').height($('.img_parent').width() + 'px');
$('.number').height($('.img_parent').height() + 'px');
$('.number div').height($('.number').height() / 3 + 'px');
$('.number div').css('line-height', $('.number div').height() + 'px');
$('#swiper-container').height($('#swiper-container').width() + 'px');

/* 商品类型动画 
--------------------------*/
function fnShow(){
    $(".hide_box_wrap").fadeIn();
    $('.hide_box_content').animate({ bottom: '0%' }, 400);
    $('.thumbnail').height($('.thumbnail').width() + 'px');
};
$(".choose").click(function(){
    fnShow();
});
   
$(".hide_box_void,.fa-times").click(function () {
    $('.hide_box_content').animate({ bottom: '-100%' }, 400);
    $(".hide_box_wrap").fadeOut();
});
$('.btn-danger').click(function () {
    var mark = true;//标记是否全部选中，默认全部选中

    if ($('.table').find('.act_box').length == 0) {
        $('.table').find('.red').remove();
        $('.table').append('<p class="red">请选择</p>');
        mark = false;

    } else {
        $(this).find('.red').remove();
    };

    if (mark == true) {
        //选中的业务逻辑
        $('.hide_box_content').animate({ bottom: '-100%' }, 400);
        $(".hide_box_wrap").fadeOut();
    }
});

/* 返回上一页按钮 
--------------------------*/
$('.back').click(function () {
    history.back();
});

/* ajax  点击按钮‘加入购物车’事件*
--------------------------*/
$('.add-cart').click(function () {
    getLogin();
    
    if($('.act_box').length===0){
        fnShow();    
    }else{ 
        var url = '/shopcar/shopcars/';
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    
        var ruleid = $('.act_box').attr('ruleid')
        var quantity = parseInt($('#carnum').text());
        var data = {
            'method': 'create',
            'ruleid': ruleid,
            'quantity': quantity,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
       $.ajax({
           url:url,
           type:'post',
           data:data,
           success: function(result) {
               if(result['status'] == 'ERROR')
                {
                    $().errormessage(result['msg']);
                }
                else{
                    $().messsage(result['msg']);
                } 
        },
        error: function() { // 500
            $().errormessage('server is down!');
        }
    });
}});