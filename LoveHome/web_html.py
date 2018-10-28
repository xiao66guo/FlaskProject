# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

# 为具体的HTML文件请求提供路由
from flask import Blueprint, current_app

html = Blueprint('html', __name__)

@html.route('/<file_name>')
def get_html_file(file_name):

    file_name = 'html/' + file_name
    # send_static_file: 通过指定的文件名找到指定的静态文件并封装成响应
    return current_app.send_static_file(file_name)


