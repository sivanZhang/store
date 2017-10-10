/* 
 *获取cookid数据
 */
var aProducts=JSON.parse(CookieUtil.get("products"));//商品
var oLists =$('#list_parent');

for (var i = 0; i < aProducts.length; i++) {
    if(i>0){
      oLists.append('<section class="list">'+
      '<img class="img-rounded pull-left" src="" />'+
      '<div class="details">'+
         '<div class="product_name">商品名称</div>'+
          '<div class="product_rull font-grey">商品说明</div>'+
          '<div class="pull-left">'+
              '<i class="fa fa-jpy" aria-hidden="true"></i>'+
              '<span class="product_price">价格</span>'+
          '</div>'+
          '<div class="product_numb font-grey pull-right">件数'+
         '</div>'+
     '</div>'+
  '</section>');
    };
    var aList =$('.list');
    $( aList[i]).find('img').attr('src',aProducts[i].img);
    $( aList[i]).find('.product_name').text(aProducts[i].name);
    $( aList[i]).find('.product_rull').text(aProducts[i].rule);
    $( aList[i]).find('.product_price').text(aProducts[i].Price);
    $( aList[i]).find('.product_numb').text('x'+aProducts[i].num+'件');
  }