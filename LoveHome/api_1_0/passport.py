# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


'''实现登录和注册'''
from . import api
from flask import request, jsonify, current_app
from LoveHome.utils.response_code import RET
from LoveHome import redis_store, db
from LoveHome.models import User


@api.route('/users', methods=['POST'])
def register():
    # 1、获取参数：手机号、短信验证码、密码
    data_dict = request.json
    mobile = data_dict.get('mobile')
    phonecode = data_dict.get('phonecode')
    password = data_dict.get('password')

    # 对获取的参数是否有值进行判断
    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2、取到真实的短信验证码
    try:
        real_phonecode = redis_store.get('Mobile' + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')

    if not real_phonecode:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码过期')

    # 3、进行验证码的对比
    if phonecode != real_phonecode:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码输入错误')

    # 4、初始化User模型，保存相关数据
    user = User()
    user.mobile = mobile
    user.name = mobile

    # 5、存储user模型到数据库中
    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='保存用户数据失败')

    # 6、返回数据
    return jsonify(errno=RET.OK, errmsg='注册成功')
