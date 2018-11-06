# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

'''房屋相关的视图函数'''
from LoveHome.api_1_0 import api
from LoveHome.models import Area, House, Facility
from flask import jsonify, current_app, request, g
from LoveHome.utils.response_code import RET
from LoveHome.utils.common import login_required
from LoveHome import db


'''添加新房屋信息功能'''
@api.route('/houses', methods=['POST'])
@login_required
def add_house():
    # 1、接收所有参数
    data_dict = request.json

    title = data_dict.get('title')
    price = data_dict.get('price')
    address = data_dict.get('address')
    area_id = data_dict.get('area_id')
    room_count = data_dict.get('room_count')
    acreage = data_dict.get('acreage')
    unit = data_dict.get('unit')
    capacity = data_dict.get('capacity')
    beds = data_dict.get('beds')
    deposit = data_dict.get('deposit')
    min_days = data_dict.get('min_days')
    max_days = data_dict.get('max_days')

    # 2、判断参数是否有值，并判断参数是否符合要求
    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    try:
        # 以分的方式进行保存
        price = int(float(price) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 3、初始化房屋模型，并设置数据
    house = House()
    house.user_id = g.user_id

    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 取出当前房屋内设施的列表
    facilities = data_dict.get('facility')
    # 取出当前房屋所对应的所有设施
    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存房屋信息失败')

    return jsonify(errno=RET.OK, errmsg='OK')




'''获取所有的城区信息'''
@api.route('/areas')
def get_areas():
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




