$('.easy-tree').EasyTree({
    addable: true,
    editable: true,
    deletable: true
});
$('.easy-tree').on('click touch', 'button.confirmadd', function() {

});
$('.easy-tree').on('change', '.easy-tree-editor', function() {
    var newname = $('.easy-tree-editor').val();
    var id = $('.li_selected').attr('categoryid');
    $.ajax({
        url: "/category/categories/",
        type: "post",
        data: {
            'name': newname,
            'id': id,
            'method': 'put'
        },
        context: document.body,
        success: function(data) {
            //$(this).addClass(data); 
        },
        error: function(e) {
            //
        }
    });
});
$(document).on('click', 'a.confirm', function() {
    //
    var id = $('.li_selected').attr('categoryid');
    $.ajax({
        url: "/category/categories/",
        type: "post",
        data: {
            'id': id,
            'method': 'delete',
        },
        context: document.body,
        success: function(data) {
            $(this).addClass(data);
        }
    });
});

$(document).on('click', 'a.confirm', function() {
    var id = $('#categoryid').val();
    $.ajax({
        url: "/category/categories/",
        type: "post",
        data: {
            'id': id,
            'method': 'delete',
        },
        context: document.body,
        success: function(data) {

        }
    });
});