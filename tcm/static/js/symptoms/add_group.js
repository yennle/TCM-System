$( document ).ready(function() {
    $('#group_form').on('submit',function(event){
        $.ajax({
            data:{
                name: $('#group_name').val()
            },
            type: 'POST',
            url: '/group/add'
        })
        .done(function(data){
            alert(data)
        });
        event.preventDefault();
    });
});