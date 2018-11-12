function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    // 判断用户是否登录
     $.get('/api/v1.0/session', function (resp) {
        // console.log(resp.data.name, resp.data.user_id)
        if (!(resp.data.user_id && resp.data.name)){
            location.href = '/login.html'
        }
    })

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    // 获取房屋的基本信息
    $.get('/api/v1.0/houses/' + houseId, function (resp) {
        if (resp.errno == '0'){
            // 设置房屋图片
            $('.house-info>img').attr('src', resp.data.house.img_urls[0])
            // 设置房屋标题
            $('.house-text>h3').html(resp.data.house.title)
            // 设置房屋价格
            $('.house-text span').html((resp.data.house.price/100).toFixed(2))
            console.log(resp.data.house.price)

        }else{
            alert(resp.errmsg)
        }
    })

    // TODO: 订单提交
})
