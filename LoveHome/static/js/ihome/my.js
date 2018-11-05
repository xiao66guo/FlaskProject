function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// TODO: 点击推出按钮时执行的函数
function logout() {
    
}

$(document).ready(function(){

    // 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            // 获取用户头像
            $('#user-avatar').attr('src', resp.data.avatar_url)

            $('#user-name').html(resp.data.name)
            $('#user-mobile').html(resp.data.mobile)
        } else {
            alert(resp.errmsg)
        }
    })
})
