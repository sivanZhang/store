/*
 * 分类菜单
 */
$(document).ready(function(){
    var min_Height = $('.sidebar').height();
    $('.detailed_menu').css('min-height', min_Height + 'px');
    
    var aMain = $('.main_menu');
    var aSub = $('.detailed_menu');
    for(var i=0;i<$('.main_menu').length;i++){
        //鼠标移入显示，移出隐藏
      ~function(i){                               //匿名函数立即执行
        $(aMain[i]).mouseenter(function(){
            $(aSub[i]).show();
          });
          $(aMain[i]).mouseleave(function(){
              $(aSub[i]).hide();
          }); 
      }(i);
    };  
    aSub.mouseenter(function(){
        $(this).show();
      });
      aSub.mouseleave(function(){
        $(this).hide();
      });
});