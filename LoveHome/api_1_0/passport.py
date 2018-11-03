# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


'''实现登录和注册'''
from . import api
from flask import request, jsonify, current_app, session
from LoveHome.utils.response_code import RET
from LoveHome import redis_store, db
from LoveHome.models import User
import re


@api.route('/session', methods=['POST'])
def login():
    # 1、获取参数
    data_dict = request.json
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')
    print mobile

    # 2、校验参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 校验手机号是否正确
    if not re.match('^1[34578][0-9]{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='请输入正确的手机号')

    # 3、通过参数mobile查询指定的用户
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='当前用户不存在')

    # 4、校验密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='密码错误')

    # 5、保存用户信息到 session 中
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile

    # 6、给出响应
    return jsonify(errno=RET.OK, errmsg='登录成功')



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
    # 保存密码
    user.password = password

    # 5、存储user模型到数据库中
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户数据失败')

    # 6、返回数据
    return jsonify(errno=RET.OK, errmsg='注册成功')
