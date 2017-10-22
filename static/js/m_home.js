$('.submenu img').height($('.submenu img').width());
$(".search").css("border-radius", $('.search').height() + 'px');
$(".fa-search").css("line-height", $('.search').height() + 'px');
//轮播图 宽高比
$('#swiper-container').height($('#swiper-container').width() * 0.6 + 'px');

 var mySwiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    prevButton: '.swiper-button-prev',
    nextButton: '.swiper-button-next',
    autoplay: 3000,
    speed: 300,
});
var mySwiper2 = new Swiper('.swiper-container-2', {
    pagination: '.swiper-pagination2',
    prevButton: '.swiper-button-prev2',
    nextButton: '.swiper-button-next2',
});
