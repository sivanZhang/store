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

//添加型号
$('#tb_rule').on('click', '.fa-trash-o', function() {

    //this.parentNode.parentNode.outerHTML = '';
    $(this).parent().parent().remove();

});
$('.btn-test').click(function() {

    var rule_el = document.getElementById('tb_rule');
    var name = $('#name').val();
    var price = $('#price').val();
    var rule = $('#rule').val();
    var inventory = $('#inventory').val();
    if (name.length == 0) {
        return;
    }

    var newhtml = ' <tr>' +
        '<td>' + name + '</td>' +
        '<td>' + price + '</td>' +
        '<td>' + rule + '</td>' +
        '<td>' + inventory + '</td>' +
        ' <td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        ' </tr>';

    rule_el.innerHTML = rule_el.innerHTML + newhtml;


});


//添加属性
$('#add-pro').click(function() {
    var addPro = document.getElementById('add-pro');
    var pro = $('#pro').val(),
        val = $('#val').val;
    var proTr = '<tr>' +
        '<td>' + pro + '</td>' +
        '<td>' + val + '</td>' + ' <td><i class="fa fa-trash-o" aria-hidden="true"></i></td>' +
        '</tr>';
    $('#my-tb').append(proTr);

    addPro.innerHTML = addPro.innerHTML + newhtml;
});
$('#my-tb').on('click', '.fa-trash-o', function() {


    $(this).parent().parent().remove();

});