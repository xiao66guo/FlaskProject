# -*- coding:utf-8 -*-


__author__ = 'xiaoguo'


from LoveHome.api_1_0 import api
from LoveHome.models import Area
from flask import jsonify, current_app
from LoveHome.utils.response_code import RET


'''房屋相关的视图函数'''

@api.route('/areas')
def get_areas():
    # 获取说有的城区信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    # 定义一个空列表，用于保存遍历时所转换的字典
    areas_dict_list = []
    # 模型转字典
    for area in areas:
        areas_dict_list.append(area.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_dict_list)




