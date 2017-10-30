
//  规格设置    >>> 删除行
$('#tb_rule').on('click', '.fa-trash-o', function () {
    $(this).parents('tr').remove();
});

//  规格设置    >>> 添加
var rule_el, name, price, rule, inventory,newhtml,html;
//表单数字输入验证
fnLimited($('#price,#inventory,.inv>input,.price>input'));

$('.add-inp input').focus(function(){
    $(".alert-text").remove();
})

$('.add-rule').click(function () {
    rule_el = document.getElementById('tb_rule');
    name = $('#name').val();
    price = $('#price').val();
    rule = $('#rule').val();
    inventory = $('#inventory').val();
    newhtml = ' <tr class="tr_rule" ruleid="-1">' +
    '<td class="hasbiil">无</td>'+
    '<td class="name"><input type="text" value="' + name + '"/></td>' +
    '<td class="unit"><input type="text" value="' + rule + '"/></td>' +
    '<td class="price"><input type="text" value="' + price + '"/></td>' +
    '<td class="inv" ><input type="text" value="' + inventory + '"/></td>' +
    '<td class="operate"><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
    '</tr>';

    if (name.length == 0 || price.length == 0 || rule.length == 0 || inventory.length == 0) {
        var html = '<div class="alert-text">内容不能为空!</div>';
        $('#tb_rule').before(html);
    }else {
        rule_el.innerHTML = rule_el.innerHTML + newhtml;
    };
    
});

//  发表+存稿按钮    >>> 点击事件
$('.submit button').click(function () {
    //loading样式
    var options = {
        theme: "sk-doc",
        message: '提交中...',
        backgroundColor: "#000",
        textColor: "white"
    };
    HoldOn.open(options);//loadding函数调用
    var categoryid = $('#sel-category').val();
    var title = $('#title').val();
    var desc = $('#desc').val();
    var detail = tinymce.get("detail").getContent();
    var obj = {};
    var rules = Array();
    var product = $('#productid');
    var rules_tr = $('.tr_rule');
    rules_tr.each(function () {
        if (product.length > 0) {
            // 修改
            obj['ruleid'] = $(this).attr('ruleid');
            obj['name'] = $(this).find('.name>input').val();
            obj['unit'] = $(this).find('.unit>input').val();
            obj['price'] = $(this).find('.price>input').val();
            obj['inv'] = $(this).find('.inv>input').val();
        }
        else {
            //新建
            obj['name'] = $(this).find('.name').text();
            obj['unit'] = $(this).find('.unit').text();
            obj['price'] = $(this).find('.price').text();
            obj['inv'] = $(this).find('.inv').text();
        }

        rules.push(obj);
        obj = {};
    });
    var parameters = Array();
    var parameters_tr = $('.parameter_tr');
    var obj_para = {};
    parameters_tr.each(function () {
        obj_para['key'] = $(this).find('.key>input').val();
        obj_para['value'] = $(this).find('.value>input').val();
        parameters.push(obj_para);
        obj_para = {};
    });


    data = {
        'method': 'create',
        'categoryid': categoryid,
        'title': title,
        'description': desc,
        'detail': detail,
        'rules': JSON.stringify(rules),
        'parameters': JSON.stringify(parameters),
        'status': $(this).attr('status'),
        'csrfmiddlewaretoken': getCookie('csrftoken'),
    };
    if (product.length > 0) {
        //3
        data['id'] = product.val();
        data['method'] = 'put'; //修改产品
    }

    var html = '<div class="alert alert-danger" role="alert">####</div>';
    $.ajax({
        type: 'post',
        url: '/product/products/',
        data: data,
        success: function (result) {
            HoldOn.close();
            $('.msg').append(html.replace('###', result['msg']));
        },
        error: function () {
            HoldOn.close();
            // 500
            alert('server is down!')
        }
    })
});

//  属性设置    >>> 添加属性
$('#add-pro').click(function () {
    $(".alert-text").remove();
    var pro = $('#pro').val();
    var val = $('#val').val();
    var proTr = '<tr class="parameter_tr">' +
        '<td class="key "><input type="text" value="' + pro + '"/></td>' +
        '<td class="value "><input type="text" value="' + val + '"/></td>' +
        '<td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        '</tr>';

    if (pro.length == 0 || val.length == 0) {
        var html = '<div class="alert-text">内容不能为空!</div>';
        $('#pro-table').before(html);
    } else {
        $('#pro-table').append(proTr);
        $('#pro,#val').val("");
    };
});

//  属性设置    >>> 删除行
$('#pro-table').on('click', '.fa-trash-o', function () {
    $(this).parent().parent().remove();
});

//  内容简介    >>> 输入字数监听     
$(".ta-wrap input").on('keyup input', function (event) {

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

///以下是修改product时用到的js
