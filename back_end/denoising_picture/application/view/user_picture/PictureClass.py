from application import db, model
import os


class UserPicture(object):
    user_list = None
    user_id: int

    def query_in_page(self, page, per_page):
        return self.user_list.paginate(page=page, per_page=per_page)

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
        if os.path.exists(os.getcwd() + self.user_origin_path):
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


class UserProcessedPicture(UserPicture):
    user_process_path: str

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_list = model.ProcessPicture.query.filter_by(owner_id=user_id)
        self.user_origin_path = f'/static/user/{self.user_id}/process/'
        if os.path.exists(os.getcwd() + self.user_origin_path):
            os.makedirs(os.getcwd() + self.user_origin_path)

    def generate_picture(self):
        pass


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
