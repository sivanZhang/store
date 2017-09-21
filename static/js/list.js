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