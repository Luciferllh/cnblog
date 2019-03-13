$('.login_btn').on('click',function () {
        $.ajax({
            url:'',
            type:'post',
            data:{
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                user:$('#user').val(),
                pwd:$('#pwd').val(),
                valid_code:$('#valid_code').val()
            },
            success:function (data) {
                console.log(data)
                if (data.state){
                    location.href='/index/'
                }
                else {
                    $('.errors').text(data.msg)
                }
            }
            }

        )
    })
    // 验证码刷新
    $('.valid').on('click',function () {
        $.ajax({
            url:'/get_vail_img/',
            type: 'get',
            success:function (data) {
                $('.valid').attr('src',"/get_vail_img/") //jQuery对象
                $('.valid')[0].src="/get_vail_img/"  //dom对象
            }
        })
     })

     // $('.valid').on('click',function () {
     //    $(this)[0].src+='?'
     // })