# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from LoveHome.api_1_0 import api
from flask import request, jsonify, current_app, g
from LoveHome.utils.response_code import RET
import datetime
from LoveHome.models import Order, House
from LoveHome.utils.common import login_required
from LoveHome import db


'''添加新订单功能'''
@api.route('/orders', methods=['POST'])
@login_required
def create_order():

    # 1、获取房屋的ID、入住开始时间和结束时间
    data_dict = request.json
    house_id = data_dict.get('house_id')
    start_date_str = data_dict.get('start_date')
    end_date_str = data_dict.get('end_date')

    # 2、对接收的参数进行校验
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 判断参数
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        if start_date and end_date:
            assert start_date < end_date, Exception('结束日期必须大于开始日期')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 判断房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='未查询到房屋数据')

    # 3、判断当前房屋在当前时间段内是否被预定
    try:
        conflict_orders_list = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据错误')
    if conflict_orders_list:
        return jsonify(errno=RET.HOUSEBOOKED, errmsg='当前房屋已被预定')

    # 4、创建订单模型并设置数据
    order = Order()
    days = (end_date - start_date).days
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = days * order.house_price
    # 设置订单的房屋数量 + 1
    house.order_count += 1

    # 5、将数据添加到数据库中
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存订单失败')

    return jsonify(errno=RET.OK, errmsg='OK')
