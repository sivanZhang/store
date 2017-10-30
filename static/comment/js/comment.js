/* 
 * 缩略图展示
 */
$('ul.thumbnail_list').on('click','a.thumbnail',function(){
    var smallAttr = $(this).children().attr('src');
    var bigAttr = $('#big_img').attr('src');
    if(smallAttr==bigAttr){
        $('#big_img').attr('src','');
    }else{
        $('#big_img').attr('src',smallAttr);
    }
    if($('#big_img').attr('src')==''){
        $('#big_img').css('display','none');
    }else{
        $('#big_img').css('display','block');
    }
});

/* 
 * 切换筛选菜单
 */
$('.nav-tabs li').click(function(){
    $(this).siblings().removeClass('active');
    $(this).addClass('active');
})

/* 
 * 点赞
 */
$('.fa-thumbs-up').click(function(){
   var num = $(this).children().text()-0;

   $(this).children('span').text(num+1);
})
/* 
 * star
 */
$('.fa-star').click(function(){
    $('.fa-star').removeClass('red_star');
    $(this).prevAll().addClass('red_star');
    $(this).addClass('red_star');
})
/* 
 * 全部评论数量
 */
var allNum = $('.com_content').length;
$('#all_num').text(allNum);

/* 
 * 发表、删除、修改评论
 */
$('button.publish').click(function () {
    var content = $('textarea').val();
    var rating = $('.red_star').length;
    data = {
        'method': 'post',
        'content': content,
        'id':1,
        'rating':rating,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax({
        type:'post',
        url:'/comment/comment/',
        data:data,
        success: function (result) {
            if (result['status'] == 'ok') {
                alert('success!');
            }
        },
        error: function () {
            alert('server is down!')
        }
    });
});
