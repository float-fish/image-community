from flask import Blueprint, request, jsonify, session, send_file, send_from_directory
from application import db, model
from . import PictureClass
from application.util.launch import generate_processed_picture
import os

bp = Blueprint('picture', __name__, url_prefix='/user/picture')


@bp.post('/process')
@bp.post('/origin')
@bp.post('/origin_collective')
@bp.post('/process_collective')
def show_picture():
    user_id = session.get('user_id')
    cur_page = request.get_json()
    page = cur_page.get('page')
    # per_page = cur_page.get('per_page')  # 这个不一定需要

    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    pictures = pic.query_in_page(page, 8)

    pictures_path = []
    pictures_id = []
    for i in pictures:
        pictures_path.append(i.picture_path)
        pictures_id.append(i.picture_id)

    return jsonify(
        {
            "code": 200,
            'msg': '成功返回当前图片页面',
            'data': {
                "pictures_path": pictures_path,
                "pictures_id": pictures_id
            }
        }
    )


@bp.get('/origin/<int:pid>')
@bp.get('/origin_collect/<int:pid>')
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
@bp.get('/process_collective/<int:pid>')
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


@bp.delete('/process/<int:pid>')
@bp.delete('/origin/<int:pid>')
def del_picture(pid: int):
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(pid)

    if picture:
        path = picture.picture_path
        os.remove(path)
        db.session.delete(picture)
        db.session.commit()
        return jsonify(code=200, msg='成功删除')
    else:
        return jsonify(code=404, msg='图片未找到'), 404


@bp.post('/process/<int:pid>')
@bp.post('/origin/<int:pid>')
def change_pname(pid: int):
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(pid)

    data = request.get_json()
    name = data.get('name')
    collect = data.get('collective_tag')
    picture.picture_name = name
    picture.collective_tag = collect
    db.session.add(picture)
    db.session.commit()
    return jsonify(code=200, msg='成功修改图片信息')


@bp.post('/transform')
def implement():
    user_id = session.get('user_id')
    user_name: str = str(session.get('user_name'))
    data = request.get_json()
    pid = data.get('pid')
    picture = model.OriginPicture.query.filter_by(picture_id=pid).first()
    size = model.ProcessPicture.query.count()
    size += 1
    entry_path = picture.picture_path
    output = os.getcwd() + f'/statics/user/{user_id}/process/'
    if not os.path.exists(output):
        os.makedirs(output)
    output += user_name + str(size) + '.jpg'
    generate_processed_picture(entry_path, output)
    processed_picture = model.ProcessPicture(picture_path=output, picture_name=user_name + str(size),
                                             picture_accuracy=80, picture_clarity=80, origin_picture_id=pid,
                                             owner_id=user_id)
    db.session.add(processed_picture)
    db.session.commit()
    return jsonify(
        {
            "code": 200,
            'msg': '成功生成图片',
            'path': output
        }
    )


@bp.post('/origin_upload')
def add_picture():
    user_id = session.get('user_id')
    image = request.files['image']
    name = request.files['image'].filename
    directory = os.getcwd()
    path = f'\\static\\user\\{user_id}\\origin'
    if not os.path.exists(directory + path):
        os.makedirs(directory + path)
    path = path + '\\' + name
    image.save(directory + path)
    picture = model.OriginPicture(picture_path=path, picture_name=name, owner_id=user_id)
    db.session.add(picture)
    db.session.commit()
    return jsonify(code=200, msg="上传成功")


@bp.post('/process/download')
@bp.post('/origin/download')
def download_picture():
    image_id = request.get_json().get('pid')
    user_id = session.get("user_id")
    picture_type = request.path.split('/')[3]
    try:
        pic: PictureClass.UserPicture = PictureClass.picture_map[picture_type](user_id=user_id)
    except TypeError:
        return jsonify(code=400, msg='路径出现错误')
    picture = pic.query_detail(image_id)
    path = picture.picture_path
    return send_file(path, as_attachment=True)


@bp.route('/<path:filename>')
def send_from_backend(filename):
    return send_from_directory(directory=os.getcwd(), path=filename)