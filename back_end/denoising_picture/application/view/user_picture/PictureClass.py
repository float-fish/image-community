from sqlalchemy import and_

from application import db, model
from datetime import datetime
import os


class UserPicture(object):
    user_list = None
    user_id: int

    def query_in_page(self, page, per_page):
        return self.user_list.paginate(page=page, per_page=per_page)

    def time_search_query_in_page(self, page, per_page, start_time, end_time):
        pass

    def query_detail(self, pid):
        return self.user_list.filter_by(picture_id=pid).first()

    def query_collective(self):
        return self.user_list.filter_by(collective_tag=True).all()


class UserOriginPicture(UserPicture):
    user_origin_path: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_list = model.OriginPicture.query.filter_by(owner_id=user_id)
        self.user_origin_path = f'/static/user/{self.user_id}/origin/'
        if not os.path.exists(os.getcwd() + self.user_origin_path):
            os.makedirs(os.getcwd() + self.user_origin_path)

    def add_picture(self, image, filename: str):
        allow_houzhui = ['png', 'jpg', 'PNG', 'JPG']
        if filename.split('.')[1] not in allow_houzhui:
            code = 400
            msg = '上传文件的格式为非图片'
            return [code, msg]
        path = self.user_origin_path + filename
        image.save(os.getcwd() + path)
        picture = model.OriginPicture(picture_path=path, picture_name=filename, owner_id=self.user_id)
        db.session.add(picture)
        db.session.commit()
        code = 200
        msg = '上传成功'
        return [code, msg]

    def time_search_query_in_page(self, page, per_page, start_time: datetime, end_time: datetime):
        print(type(model.OriginPicture.update_time))
        return (self.user_list.filter(and_(start_time <= model.OriginPicture.update_time,
                                           model.OriginPicture.update_time <= end_time))
                .paginate(page=page, per_page=per_page))


class UserProcessedPicture(UserPicture):
    user_process_path: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_list = model.ProcessPicture.query.filter_by(owner_id=user_id)
        self.user_origin_path = f'/static/user/{self.user_id}/process/'
        if not os.path.exists(os.getcwd() + self.user_origin_path):
            os.makedirs(os.getcwd() + self.user_origin_path)

    def generate_picture(self):
        pass

    def time_search_query_in_page(self, page, per_page, start_time, end_time):
        return (self.user_list.filter(and_(start_time <= model.ProcessPicture.generate_time,
                                           model.ProcessPicture.generate_time <= end_time))
                .paginate(page=page, per_page=per_page))


class OriginCollective(UserPicture):

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_list = model.OriginPicture.query.filter_by(owner_id=user_id).filter_by(collective_tag=True)


class ProcessedCollective(UserPicture):

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_list = model.ProcessPicture.query.filter_by(owner_id=user_id).filter_by(collective_tag=True)


picture_map = {
    'origin': UserOriginPicture,
    'process': UserProcessedPicture,
    'origin_collective': OriginCollective,
    'process_collective': ProcessedCollective
}
