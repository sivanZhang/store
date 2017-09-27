    /* 商品类型动画 */
    $(".choose,.add-cart").click(function () {
        $(".hide_box_wrap").fadeIn();
        $('.hide_box_content').animate({ bottom: '0%' }, 400);
        $('.thumbnail').height($('.thumbnail').width() + 'px');
    });
    $(".hide_box_void,.fa-times").click(function () {
        $('.hide_box_content').animate({ bottom: '-100%' }, 400);
        $(".hide_box_wrap").fadeOut();
    });
    $('.btn-danger').click(function(){
        var mark = true;//标记是否全部选中，默认全部选中
        $('.rule_wrap').each(function(){
            if($(this).children('.act_box').length==0){
              $(this).find('.red').remove();
              $(this).append('<p class="red">请选择</p>');
              mark = false;
                
            } else{
                $(this).find('.red').remove();
            }
        })

        if (mark == true){
            //选中的业务逻辑
            $('.hide_box_content').animate({ bottom: '-100%' }, 400);
            $(".hide_box_wrap").fadeOut();
        }
        
      
               
        
    });

    /* 商品类型动画 end*/
      
    
    /* 选中规格效果
    ------------------------------------------------- */
    $('.rule_box').click(function () {
        $(this).siblings().removeClass('act_box');
        $(this).addClass('act_box');
    });