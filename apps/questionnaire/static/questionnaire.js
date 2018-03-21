
var answers=new Array();

$(function () {
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