
$(function () {
    //提交表单
    //邮箱注册
    $('#btnQuestionnaire').on('click',function(){
        $.ajax({
            cache: false,
            type: "POST",
            url: "{% url 'questionnaire:add_questionnaire' %}",
            data: {
                questionnaire_id:{{ questionnaire.id }}
            },
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
        },
        success: function (data) {
            if (data.status == 'fail') {
              if (data.msg == '用户未登录') {
                  window.location.href = "{% url 'login' %}";
              } else {
                  alert(data.msg)
              }
            } else if (data.status == 'success') {
                alert('评论成功！')
                window.location.reload();//刷新当前页面.
            }
        },
        error: function(error) {
          alert('ajax 失败!')
        }
    });
    });
    //单选
    $("input[type='radio']").change(function(){
        console.log($(this).val());

    });
    //多选
    $("input[type='checkbox']").change(function(){
        console.log($(this).val());
    });
    //问答
    $(".question_ask_text").change(function(){
        console.log($(this).val());
    });
    //打星
});