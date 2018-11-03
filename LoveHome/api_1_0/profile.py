# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from . import api
from flask import session, current_app, jsonify
from LoveHome.models import User
from LoveHome.utils.response_code import RET


@api.route('/user')
def get_user_info():

    # 1、获取当前登录的用户ID
    user_id = session.get('user_id')

    # 2、查询出指定的用户信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 3、组织数据，进行返回
    resp = {
        'name': user.name,
        'avatar_url': user.avatar_url,
        'user_id': user.id
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=resp)


