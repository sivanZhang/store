/*
 * Demo3:label样式
 */
$("#img_input2").on("change", function(e) {

    var file = e.target.files[0]; //获取图片资源

    // 只选择图片文件
    if (!file.type.match('image.*')) {
        return false;
    }

    var reader = new FileReader();

    reader.readAsDataURL(file); // 读取文件

    // 渲染文件
    reader.onload = function(arg) {

        var img = '<img class="preview" src="' + arg.target.result + '" alt="preview"/>';
        $("#preview_box2").empty().append(img);
    }
});


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

$(document).ready(function(){
    $('.btn-set-primary').click(function(){
        var btn = $(this);
        var picid = btn.attr('picid');
        var productid = btn.attr('productid');
        var formData = new FormData(document.querySelector("#csrftocken_form")); 
        formData.append('picid', picid);
        formData.append('productid', productid);
        $.ajax('/product/products/'+productid+'/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
            if (data['status'] == 'OK') {
                    $().message(data['msg']);
                }
                else {
                    $().errormessage(data['msg']);
                }
            },
            error: function () {
                $().errormessage('server side error');
            }
        });
    });
    $('.btn-delete-primary').click(function(){
        var btn = $(this);
        var picid = btn.attr('picid');
        var productid = btn.attr('productid');
        var formData = new FormData(document.querySelector("#csrftocken_form")); 
        formData.append('picid', picid);
        formData.append('productid', productid);
        formData.append('method', 'delete');
        $.ajax('/product/products/'+productid+'/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
            if (data['status'] == 'OK') {
                    $().message(data['msg']);
                }
                else {
                    $().errormessage(data['msg']);
                }
            },
            error: function () {
                $().errormessage('server side error');
            }
        });
    });
});