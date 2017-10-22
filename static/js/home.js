
 var mySwiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    prevButton: '.swiper-button-prev',
    nextButton: '.swiper-button-next',
    autoplay: 3000,
    speed: 300,
});

/*
 * 分类菜单
 */
var min_Height = $('.sidebar').height();
$('.detailed_menu').css('min-height', min_Height + 'px');

var aMain = $('.main_menu');
var aSub = $('.detailed_menu');
for(var i=0;i<$('.main_menu').length;i++){
    //鼠标移入显示，移出隐藏
  ~function(i){
    $(aMain[i]).mouseenter(function(){
        $(aSub[i]).show();
      });
  
      $(aMain[i]).mouseleave(function(){
          $(aSub[i]).hide();
      }); 
  }(i);//匿名函数立即执行
};  
aSub.mouseenter(function(){
    $(this).show();
  });
  aSub.mouseleave(function(){
    $(this).hide();
  });
$('.swiper-slide').css('max-height', min_Height + 'px');