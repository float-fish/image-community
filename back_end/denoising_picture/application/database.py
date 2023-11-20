from application import model, db, app

with app.app_context():
    # 增
    # user = model.HeadPicture(head_picture_path='C:/user/picture')
    # db.session.add(user)
    # db.session.commit()

    # db.session.add_all([])

    # 查
    # head = model.HeadPicture.query.get(1)
    # print(head)

    # heads = model.HeadPicture.query.all()
    # for h in heads:
    #     print(h.head_picture_path)

    # condition = model.HeadPicture.query.filter(model.HeadPicture.head_picture_id > 2)
    # for h in condition:
    #     print(h.head_picture_id)
    #
    # condition = model.HeadPicture.query.filter_by(head_picture_id=2).all()
    # print(condition)

    # 改
    # update = model.HeadPicture.query.get(1)
    # update.head_picture_path = 'D:/图片'
    # db.session.add(update)
    # db.session.commit()

    # 删除
    # dele = model.HeadPicture.query.filter(model.HeadPicture.head_picture_id >= 3).delete()
    # db.session.commit()
    pass
