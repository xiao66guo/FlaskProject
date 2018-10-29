# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

# 图片验证码和短信验证码的处理
from . import api
from LoveHome.utils.captcha.captcha import captcha


@api.route('/image_code')
def get_image_code():
    # 生成图片验证码
    name, text, image = captcha.generate_captcha()
    # 返回图片验证码的图片
    return image