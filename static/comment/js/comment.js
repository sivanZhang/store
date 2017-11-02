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
});//缩略图展示end

/* 
 * 切换筛选菜单
 */
$('.nav-tabs li').click(function(){
    $(this).siblings().removeClass('active');
    $(this).addClass('active');
})

/* 
 * star
 */
$('.star>.fa-star').click(function(){
    $('.star>.fa-star').removeClass('red_star');
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
//发表评论
$('button.publish').click(function () {
    var content = $('#com_textarea').val();
    var rating = $('.star .red_star').length;
    var productid=$('#productid').val();
    var id = productid;
    data = {
        'method': 'post',
        'content': content,
        'id':id,
        'rating':rating,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax({
        type:'post',
        url:'/comment/comment/',
        data:data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $().message(result['msg'] );
            }
            else{
                $().errormessage(result['msg'] );
            }
        },
        error: function () {
            alert('server is doffwn!')
        }
    });
});
//回复评论
$('button.reply_btn').click(function () {
    var content = $(this).siblings('.reply_textarea').val();
    var parentid =  $(this).parent().siblings('.commenting').attr('commentid');
    var productid=$('#productid').val();
    var id = productid;
    data = {
        'method': 'post',
        'content': content,
        'id':id,
        'parentid':parentid,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax({
        type:'post',
        url:'/comment/comment/',
        data:data,
        success: function (result) {
            if (result['status'] == 'ok') {
                $('.reply').hide();
            }
        },
        error: function () {
            alert('server is doffwn!')
        }
    });
});
//删除回复
$('.txt_delete').click(function () {
    var thisBtn=$(this);
    var commentid =  $(this).parent('.reply_list').attr('data-com-id');
    data = {
        'method': 'delete',
        'id':commentid,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    };
    $.ajax({
        type:'post',
        url:'/comment/comment/',
        data:data,
        success: function (result) {
            if (result['status'] == 'ok') {
                thisBtn.parent().remove();
            }
        },
        error: function () {
            alert('server is doffwn!')
        }
    });
});

/* 
 * 回複评论
 */
 $('#comment').on('click','.fa-commenting',function(){
    $(this).parent().siblings('.reply').show();
})
$('#comment').on('click','.txt_commenting',function(){
    $(this).parent().siblings('.reply').show();
})

/* 
 * 服务器返回数据，星星显示
 */
var aRating=$('.rating');
for(var i = 0;i<aRating.length;i++)
{
    var star_num = $(aRating[i]).attr('data-rating')-0;
    for(var j = 0;j<star_num;j++){
        $(aRating[i]).append('<i class="fa fa-star" aria-hidden="true"></i>');
    }
}; 
/* 
 * 回复数量
 */ 
/* var allReply = $('.com_content').length;
$('#all_num').text(allReply); */
