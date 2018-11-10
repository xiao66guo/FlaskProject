# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

'''房屋相关的视图函数'''
from LoveHome.api_1_0 import api
from LoveHome.models import Area, House, Facility, HouseImage
from flask import jsonify, current_app, request, g, session
from LoveHome.utils.response_code import RET
from LoveHome.utils.common import login_required
from LoveHome import db, constants, redis_store
from LoveHome.utils import image_storage


'''获取首页推荐房屋'''
@api.route('/houses/index')
def get_house_index():
    try:
        houses = House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)

    houses_dict_list = []
    # 遍历将房屋模型列表转换成字典
    for house in houses:
        houses_dict_list.append(house.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=houses_dict_list)





'''显示房屋详情信息'''
@api.route('/houses/<int:house_id>')
def get_house_detail(house_id):
    # 1、通过房屋ID查询指定的房屋模型
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')
    if not house:
        return jsonify(RET.NODATA, errmsg='房屋不存在')
    # 2、封装房屋字典信息
    resp_dict = house.to_full_dict()
    # 取到当前登录用户的ID，如果没有用户登录就返回-1
    user_id = session.get('user_id', -1)

    return jsonify(errno=RET.OK, errmsg='OK', data={'house': resp_dict, 'user_id': user_id})



    return jsonify(errno=RET.OK, errmsg='OK')


'''上传房屋图片功能'''
@api.route('/house/image', methods=['POST'])
@login_required
def upload_house_image():
    # 1、获取房屋的图片和id
    try:
        house_image = request.files.get('house_image').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 获取房屋的id
    house_id = request.form.get('house_id')
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2、获取到指定房屋id对应的房屋模型
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋数据失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='当前房屋不存在')

    # 3、上传图片到七牛云
    try:
        key = image_storage.upload_image(house_image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传房屋图片失败')

    # 判断当前房屋是否设置index_image_url,如果没有设置直接设置
    if not house.index_image_url:
        house.index_image_url = key

    # 4、初始化房屋图片的模型
    house_image_model = HouseImage()

    # 5、设置数据并保存到数据库中
    house_image_model.house_id = house_id
    house_image_model.url = key

    try:
        db.session.add(house_image_model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存房屋数据失败')

    # 6、返回图片数据
    return jsonify(errno=RET.OK, errmsg='房屋图片上传成功', data={'image_url': constants.QINIU_DOMIN_PREFIX + key})


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
        deposit = int(float(deposit) * 100)

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

    return jsonify(errno=RET.OK, errmsg='OK', data={'house_id': house.id})


'''获取所有的城区信息'''
@api.route('/areas')
def get_areas():

    # 先从redis缓存中获取城区信息
    try:
        areas_dict_list = redis_store.get('Areas')
        if areas_dict_list:
            return jsonify(errno=RET.OK, errmsg='OK', data=eval(areas_dict_list))
    except Exception as e:
        current_app.logger.error(e)

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

    # 缓存城区信息到redis中
    try:
        redis_store.set('Areas', areas_dict_list, constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_dict_list)




