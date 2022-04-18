$(function (){
    var flag = false;
    var reg = /^BV[A-Za-z0-9]{10}$/

    $("#BVNumberInput").blur(function () {
        if($(this).val().length == 12 && reg.test($(this).val())) {
            flag = true;
        } else {
            $("#BVNumberHelp").css("color","red");
        }
    })

    $("#submit_btn").click(function () {
        if(flag) {
            $("#BVNumberHelp").html("<h4>正在爬取中...</h4>");
            $('from').submit();
        } else {
            $("#BVNumberHelp").html("<h4 style='color: red'>格式不正确！</h4><br>BV号格式：BV(大写)" +
                "+数字或大小写字母十位<br>示例：BV1RY411g7sK").css("color","red");
            return false;
        }
    })
})