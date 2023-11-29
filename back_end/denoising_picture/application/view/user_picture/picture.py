#!/usr/bin/env python3.11.4
""" 对前端页面实现用户个人图库操作的api接口

Copyright 2023 Yu Shengjie.
License(GPL)
Author: Yu Shengjie
"""
import os
from datetime import datetime
from math import ceil

from flask import Blueprint, request, jsonify, session, send_file, send_from_directory

from application import db, model
from application.util.launch import generate_processed_picture
from . import PictureClass

bp = Blueprint('picture', __name__, url_prefix='/user/picture')


@bp.route('/process', methods=['GET', 'POST'])
@bp.route('/origin', methods=['GET', 'POST'])
@bp.route('/origin_collective', methods=['GET', 'POST'])
@bp.route('/process_collective', methods=['GET', 'POST'])
def show_picture():
    user_id = session.get('user_id')
    print(session.get('user_id'))

    cur_page = request.get_json()
    if 'user_id' in cur_page:
        user_id = cur_page.get('user_id')
    page: int = cur_page.get('page')
    if not page:
        return jsonify(code=400, msg='错误!参数page为空'), 400
    per_page = 8
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    pictures = pic.query_all()
    picture_num = pic.query_count()
    current_num = min(per_page, picture_num - (page - 1) * per_page)
    total_page = ceil(picture_num / per_page)

    picture_information = dict()
    picture_time = dict()
    for i in pictures:
        picture_information[i.picture_id] = i.picture_path
        if type(i) is model.OriginPicture:
            picture_time[i.picture_id] = i.update_time.strftime("%Y-%m-%d_%H:%M:%S")
        else:
            picture_time[i.picture_id] = i.generate_time.strftime("%Y-%m-%d_%H:%M:%S")

    return jsonify(
        {
            "code": 200,
            'msg': f'成功返回当前{page}页图片页面',
            'data': {
                "pictures_information": picture_information,
                "pictures_time": picture_time,
                'current_num': current_num,
                'total_page': total_page
            }
        }
    )


@bp.route('process/time_search', methods=['GET', 'POST'])
@bp.route('origin/time_search', methods=['GET', 'POST'])
def time_search():
    user_id = session.get('user_id')
    data = request.get_json()
    if 'user_id' in data:
        user_id = data.get('user_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    # page = data.get('page')
    # per_page = 8
    if not all([user_id, start_time, end_time]):
        print('参数不完整')
        return jsonify(code=400, msg='传递参数不完整'), 400
    start = datetime.strptime(start_time, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    end = datetime.strptime(end_time, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    # print(start, end, type(start))
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    pictures = pic.query_time_all(start, end)
    picture_num = pic.query_count()
    # current_num = min(per_page, picture_num - (page - 1) * per_page)
    # total_page = ceil(picture_num / per_page)

    pictures_path = []
    pictures_id = []
    pictures_time = []
    for i in pictures:
        pictures_path.append(i.picture_path)
        pictures_id.append(i.picture_id)
        if type(i) is model.OriginPicture:
            pictures_time.append(i.update_time.strftime("%Y-%m-%d_%H:%M:%S"))
        else:
            pictures_time.append(i.generate_time.strftime("%Y-%m-%d_%H:%M:%S"))

    return jsonify(
        {
            "code": 200,
            'msg': '成功返回当前图片页面',
            'data': {
                "pictures_path": pictures_path,
                "pictures_id": pictures_id,
                'pictures_time:': pictures_time,
                # 'current_num': current_num,
                # 'total_page': total_page
            }
        }
    )


@bp.get('/origin/<int:pid>')
def show_origin_detail(pid: int):
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(pid)
    return jsonify(
        {
            "code": 200,
            'msg': "成功获取图片信息",
            "data": {
                'name': picture.picture_name,
                'update_time': picture.update_time,
                'collective_tag': picture.collective_tag
            }
        }
    )


@bp.get('/process/<int:pid>')
def show_process_detail(pid: int):
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(pid)
    return jsonify(
        {
            "code": 200,
            'msg': "成功获取图片信息",
            "data": {
                'name': picture.picture_name,
                'generate_time': picture.generate_time,
                'collective_tag': picture.collective_tag,
                'clarity': picture.picture_clarity,
                'accuracy': picture.picture_accuracy
            }
        }
    )


@bp.post('/process/delete/<int:pid>')
@bp.post('/origin/delete/<int:pid>')
def del_picture(pid: int):
    user_id = session.get("user_id")
    print(user_id)
    if 'user_id' in request.get_json():
        user_id = request.get_json().get('user_id')
    if not user_id:
        return jsonify(code=400, msg='用户id为空'), 400
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路由出现错误'), 400
    picture = pic.query_detail(pid)

    if picture:
        path = os.getcwd() + picture.picture_path
        try:
            os.remove(path)
        except OSError:
            return jsonify(code=500, msg='图片路径有误'), 500
        db.session.delete(picture)
        db.session.commit()
        return jsonify(code=200, msg='成功删除')
    else:
        return jsonify(code=404, msg='图片未找到'), 404


@bp.post('/process/<int:pid>')
@bp.post('/origin/<int:pid>')
def change_picture(pid: int):
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(pid)
    if not picture:
        return jsonify(code=400, msg='找不到对应的图片')

    data = request.get_json()
    # name = data.get('name')
    collect = data.get('collective_tag')
    # picture.picture_name = name
    picture.collective_tag = collect
    db.session.add(picture)
    db.session.commit()
    return jsonify(code=200, msg='成功修改图片信息')


@bp.post('/transform')
def implement():
    user_id = session.get('user_id')
    data = request.get_json()
    if 'user_id' in data:
        user_id = data.get('user_id')
    pid = data.get('pid')
    if not all([pid, user_id]):
        return jsonify(code=400, msg='请求的参数不全'), 400
    picture = model.OriginPicture.query.filter_by(picture_id=pid).first()
    if not picture:
        return jsonify(code=400, msg=f'图片编号{pid}对应的图片不存在'), 400
    size = model.ProcessPicture.query.count()
    size += 1
    entry_path = os.getcwd() + picture.picture_path
    save_path = f'/static/user/{user_id}/process/'
    output = os.getcwd() + save_path
    if not os.path.exists(output):
        os.makedirs(output)
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H%M%S")
    name = current_time_str
    save_path += name + '.jpg'
    output = os.getcwd() + save_path
    generate_processed_picture(entry_path, output)
    processed_picture = model.ProcessPicture(picture_path=save_path, picture_name=str(user_id) + str(size),
                                             picture_accuracy=80, picture_clarity=80, origin_picture_id=pid,
                                             owner_id=user_id)

    db.session.add(processed_picture)
    db.session.commit()
    curr_pid = processed_picture.picture_id
    return jsonify(
        {
            "code": 200,
            'msg': '成功生成图片',
            'path': save_path,
            'pid': curr_pid
        }
    )


@bp.route('/upload', methods=['GET', 'POST'])
def add_picture():
    user_id = session.get('user_id')
    if 'user_id' in request.form:
        user_id = request.form.get('user_id')
    print(user_id)
    try:
        if len(request.files) == 0:
            print("文件是空的!!!")
            return jsonify(code=400, msg='empty picture'), 400
        for file in request.files.values():
            image = file
            name = file.filename
            print(name)
            allow_suffix = ['png', 'jpg', 'PNG', 'JPG']
            suffix = name.split('.')[1]
            if suffix not in allow_suffix:
                return jsonify(code=400, msg='error files'), 400
            directory = os.getcwd()
            path = f'/static/user/{user_id}/origin'
            if not os.path.exists(directory + path):
                os.makedirs(directory + path)
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d_%H%M%S")
            path = path + '/' + current_time_str + '.' + suffix
            image.save(directory + path)
            picture = model.OriginPicture(picture_path=path, picture_name=name, owner_id=user_id)
            db.session.add(picture)
            db.session.commit()
        return jsonify(code=200, msg="上传成功")
    except KeyError:
        return jsonify(code=400, msg='缺少对应参数的图片文件'), 400


@bp.route('origin/download')
@bp.route('process/download')
def download_picture():
    data = request.get_json()
    image_id = data.get('pid')
    user_id = session.get("user_id")
    if 'user_id' in data:
        user_id = data.get('user_id')
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(image_id)
    path = os.getcwd() + picture.picture_path
    return send_file(path, as_attachment=True)


@bp.route('/<path:filename>')
def send_from_backend(filename):
    print(filename)
    return send_from_directory(directory=os.getcwd(), path=filename)
