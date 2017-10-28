$("#fileUpload").on('change', function () {
    
       if (typeof (FileReader) != "undefined") {
    
           var image_holder = $("#image-holder");
           image_holder.empty();
    
           var reader = new FileReader();
           reader.onload = function (e) {
               $('img.thumb-image').remove();
               $("<img />", {
                   "src": e.target.result,
                   "class": "thumb-image"
               }).appendTo(image_holder);
    
           }
           image_holder.show();
           reader.readAsDataURL($(this)[0].files[0]);
       } else {
           alert("你的浏览器不支持FileReader.");
       }
   });
 $('table').on('click','.edit',function(){
     $('#add_input').empty();
      var oTr=$(this).parents('tr.table_con');
      $('#title').val(oTr.children('.b_title').children().text());
      $('#url').val(oTr.children('.b_url').children().text());
      $('#mark').val(oTr.children('.b_mark').text());
      var itemid= oTr.children('.b_itemid').text();
      $('#add_input').prepend('<input type="hidden" name="itemid" id="itemid" value="'+itemid
        +'"/>'
        +'<input type="hidden" name="method" value="put" />');
 });
 
 $('table').on('click','.fa-trash-o',function(){
     var oDelete = $(this);
    var bId=$(this).parents('tr.table_con').children('.b_itemid').text();
    var blockid  = $('#blockid').val();
    data = {
        'method': 'delete',
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'id': bId
    };
    $.ajax({
        type: 'post',
        url: '/sitecontent/blockitemcontents/?new=&blockid='+blockid,
        data:data,
        success: function (result) {    
            if (result['status'] == 'ok') {
                oDelete.parents('tr.table_con').remove();
            }
        },
        error: function () {
            alert('server is down!')
        }
    })
});


