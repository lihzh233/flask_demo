// 整个网页都加在完毕后再执行的
function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event) {
        // $this:代表的是当前按钮的jQuery对象
        var $this = $(this);
        //阻止默认的事件
        event.preventDefault();
        var email = $("input[name='email']").val();
        // alert(email);
        $.ajax({
            url: "/auth/captcha/email?email=" + email,
            method: "GET",
            success: function (result) {
                console.log(result);
                var code = result['code'];
                if (code == 200) {
                    var countdown = 60;
                    // 开始倒计时之前，就取消按钮的点击事件
                    $this.off("click");
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -= 1;
                        if (countdown <= 0){
                            // 清掉定时器
                            clearInterval(timer);
                            //将按钮文字重新修改回来
                            $this.text("获取验证码")
                            // 重新绑定点击事件
                            bindEmailCaptchaClick()
                        }

                    },1000);
                    alert("邮箱验证码发送成功！");
                }else {
                    alert(result['message'])
                }
            },
            fail: function (error) {
                console.log(error);
            }

        })
    });
}
$(function () {
    bindEmailCaptchaClick()
});
