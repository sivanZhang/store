//  搜索栏样式改变
var oForm = document.getElementById('search-form');
var oInp = oForm.firstElementChild;
oInp.addEventListener('focus', addBottom, true);

function addBottom() {
    oForm.style.cssText = 'border-bottom:1px solid #44a8f2';
    oInp.style.cssText = 'outline:none';
}
oInp.addEventListener('blur', removeBottom, false);

function removeBottom() {
    oForm.style.cssText = 'border-bottom:1px solid #FFF;'

}

//  规格设置    >>> 删除行
$('#tb_rule').on('click', '.fa-trash-o', function() {

    $(this).parent().parent().remove();

});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
        return cookieValue;
    }
    
//  规格设置    >>> 添加
$('.btn-publish').click(function() {

    var obj = {};
    var rules = Array();

    var rules_tr = $('.tr_rule');
    rules_tr.each(function() {
        obj['name'] = $(this).find('.name').text();
        obj['unit'] = $(this).find('.type').text();
        obj['price'] = $(this).find('.price').text();
        obj['inv'] = $(this).find('.inv').text();
        rules.push(obj);
        obj = {};
    });
    var parameters = Array();
    var parameters_tr = $('.parameter_tr');
    var obj_para = {};
    parameters_tr.each(function() {
        obj_para['key'] = $(this).find('.key').text();
        obj_para['value'] = $(this).find('.value').text();

        parameters.push(obj_para);
        obj_para = {};
    });
    var csrftoken = getCookie('csrftoken');
    

    data ={};
    var name = 2323;
    name = $('#name').val();
    data['name'] = name;
    var desc = '';
    desc = $('#desc').val();
    data['descsdf'] = desc;

   
});


//  属性设置    >>> 添加属性
$('#add-pro').click(function() {
    var pro = $('#pro').val();
    var val = $('#val').val();
    var proTr = '<tr>' +
        '<td>' + pro + '</td>' +
        '<td>' + val + '</td>' +
        '<td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        '</tr>';

    if (pro.length == 0 || val.length == 0) {
        pro - tablelert('内容不能为空!')
    } else {
        $('#pro-table').append(proTr);
    };
});

//  属性设置    >>> 删除行
$('#my-tb').on('click', '.fa-trash-o', function() {
    $(this).parent().parent().remove();
});

//  内容简介    >>> 输入字数监听     
$(".ta-wrap input").on('keyup  input', function(event) {
    console.log(event.type)
    var val = $(this).val();
    var len = val.length;
    var count = $(this).siblings('span');
    if (len == 0) { count.text("0/50"); return; }
    if (len > 50) {
        len = 50;
        $(this).val(val.substring(0, 50));
    }
    count.text(len + "/50");
});
/*
var categoryid = $('#select').val();
data ={
    'categoryid':categoryid,
    'title': title,
    'desc':'',
    'detail':detail,
    'rules':{},
    'parameters':{}，
    'status':'draft/publish'
    
}
$.post('/product/products/', data, function(result){
    result['status'] == 'error'
    result['msg'] //200, 500
})
$.ajax({
    url:'',
    data:data,
    success:function(){

    },
    error:function(){
        // 500
        alert('server is down!')
    }
})
*/