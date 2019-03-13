$('#div_digg .dig').click(function () {
    var username=$('.info').attr('username')
    if (username) {
        console.log(username)
        var is_up = $(this).hasClass('diggit')
        console.log(is_up)
        var article_id = $('.info').attr('article_id')

        $.ajax({
            url: '/blog/poll/',
            type: 'post',
            data: {
                is_up: is_up,
                article_id: article_id,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                console.log(data)
                if (data.state) {
                    var val = parseInt($('.diggnum').text()) + 1
                    $('.diggnum').text(val)
                } else {
                    if (data.first_action) {
                        $('.diggword').html('您已经推荐过了')
                    } else {
                        $('.diggword').html('您已经反对过了')
                    }
                    setTimeout(function () {
                        $('.diggword').html('')
                    }, 1000)
                }

            }
        })
    }
    else {
        location.href='/login/'
    }
})

