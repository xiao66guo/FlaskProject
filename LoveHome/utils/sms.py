# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from LoveHome.thirdlibs.yuntongxun.CCPRestSDK import REST
import ConfigParser
import ssl
# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 主帐号
accountSid = '8a216da866be981b0166c4ae61680527'

# 主帐号Token
accountToken = 'cbd868653e624fa984ac2a4fb9675f6b'

# 应用Id
appId = '8a216da866be981b0166c4ae61c4052e'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)


sendTemplateSMS("18811725783", ["666666", "5"], "1")