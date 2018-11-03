# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

from . import api
from flask import session, current_app, jsonify, request
from LoveHome.models import User
from LoveHome.utils.response_code import RET
from LoveHome.utils.image_storage import upload_image
from LoveHome import db, constants


'''修改用户名'''
@api.route('/user/name', methods=['POST'])
def set_user_name():
    # 1、获取传过来的用户名，并判断是否有值
    user_name = request.json.get('name')
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2、查询到当前用户
    user_id = session.get('user_id')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据出错')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='当前用户不存在')

    # 3、更新当前登录用户的模型
    user.name = user_name

    # 4、保存数据到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')

    # 5、返回响应
    return jsonify(errno=RET.OK, errmsg='保存成功')




'''上传用户图像'''
@api.route('/user/head_image', methods=['POST'])
def upload_userImage():
    # 1、获取到上传的头像
    try:
        avatar_data = request.files.get('avatar').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='读取文件失败')

    # 3、上传图片文件到七牛云
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    # 4、如果上传成功，将头像保存到用户表中的头像字段
    user_id = session.get('user_id')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 赋值到用户模型
    user.avatar_url = key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')

    # 5、返回响应，附带头像地址
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传成功', data={'avatar_url': avatar_url})




'''获取用户信息'''
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
    return jsonify(errno=RET.OK, errmsg='OK', data=user.to_dict())


