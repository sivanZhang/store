$('body').height($(window).height() + 'px');
$('.submenu img').height($('.submenu img').width());
$(".search").css("border-radius", $('.search').height() + 'px');
$(".fa-search").css("line-height", $('.search').height() + 'px');
$('#signup-Form').children().css("margin", "30px auto 5px");
$('.inp-search').focus(function() {
    $('.search').css('background-color', '#fff').css('color', '#333');
})
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