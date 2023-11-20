from flask import Blueprint, request, jsonify, session, send_file
from application import db
from .. import model
import os

bp = Blueprint('picture', __name__, url_prefix='/user/<int:id>/picture')


@bp.get('/process')
@bp.get('/origin')
def show_picture(id: int):
    cur_page = request.get_json()
    page = cur_page.get('page')
    per_page = cur_page.get('per_page')  # 这个不一定需要
    print(request.path)
    if 'origin' in request.path:
        pictures = model.OriginPicture.query.filter_by(owner_id=id).paginate(page=page, per_page=per_page)
    elif 'process' in request.path:
        pictures = model.ProcessPicture.query.filter_by(owner_id=id).paginate(page=page, per_page=per_page)
    else:
        return jsonify(code=400, msg='错误的删除请求路由'), 400

    pictures_path = []
    pictures_id = []
    for i in pictures:
        pictures_path.append(i.picture_path)
        pictures_id.append(i.picture_id)
    return jsonify(
        {
            "code": 200,
            'msg': '成功返回当前页面',
            'data': {
                "pictures_path": pictures_path,
                "pictures_id": pictures_id
            }
        }
    )


@bp.get('/origin/<int:pid>')
def show_origin_detail(pid: int, id: int):
    picture = model.OriginPicture.query.filter_by(picture_id=pid).first()
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
def show_process_detail(pid: int, id: int):
    picture = model.ProcessPicture.query.filter_by(picture_id=pid).first()
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
def del_picture(pid: int, id: int):
    if 'origin' in request.path:
        picture = model.OriginPicture.query.filter_by(picture_id=pid).first()
    elif 'process' in request.path:
        picture = model.ProcessPicture.query.filter_by(picture_id=pid).first()
    else:
        return jsonify(code=400, msg='错误的删除请求路由'), 400

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
def change_pname(pid: int, id: int):
    if 'origin' in request.path:
        picture = model.OriginPicture.query.filter_by(picture_id=pid).first()
    elif 'process' in request.path:
        picture = model.ProcessPicture.query.filter_by(picture_id=pid).first()
    else:
        return jsonify(code=400, msg='错误的更改请求路由'), 400

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
    pass


@bp.post('/origin_upload')
def add_picture(id: int):
    image = request.files['image']
    name = request.files['image'].filename
    path = os.getcwd() + f'/statics/user/{id}/origin'
    if not os.path.exists(path):
        os.mkdir(path)
    path = path+name
    image.save(path)
    picture = model.OriginPicture(picture_path=path, picture_name=name, owner_id=id)
    db.session.add(picture)
    db.session.commit()
    return jsonify(code=200, msg="上传成功")


@bp.post('/process_download')
def download_picture(id: int):
    image_id = request.get_json().get('pid')
    picture = model.ProcessPicture.query.filter_by(picture_id=image_id).first()
    path = picture.picture_path
    return send_file(path, as_attachment=True)
