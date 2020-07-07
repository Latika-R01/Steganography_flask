$(document).ready(function(){


  $('#new_encrypt').on('click', function () {
    $.ajax({
            type:'POST',
            url:'/encrypt',
//            data:{"email":email,"password":password},
            success: function (response) {
            if (response!="")
            {
             console.log(23)
        location.reload();
            }

            }
             });
    });
});
