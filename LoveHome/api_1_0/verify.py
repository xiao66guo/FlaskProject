# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

# 图片验证码和短信验证码的处理
from . import api
from LoveHome.utils.captcha.captcha import captcha
from flask import request, jsonify, make_response, abort
from LoveHome import redis_store, constants
from LoveHome.utils.response_code import RET


@api.route('/image_code')
# 图片验证码的视图函数
def get_image_code():
    # 1、取到图片验证码编码
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    if not cur_id:
        abort(403)

    # 2、生成图片验证码
    name, text, image = captcha.generate_captcha()
    # 3、将图片验证码的内容通过图片编码保存到redis中
    try:
        redis_store.set('ImageCode:'+cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete('ImageCode:'+pre_id)
    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR, errmsg='存储图片验证码数据失败')
    # 返回图片验证码的图片
    response = make_response(image)
    # 设置响应的内容类型
    response.headers['Content-Type'] = 'image/jpg'
    return response