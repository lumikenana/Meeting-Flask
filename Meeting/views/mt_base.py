from flask import Blueprint, request, jsonify, session
from Meeting import db
from Meeting import models
import json

# from . import get_session

mt_base = Blueprint('mt_base', __name__, url_prefix='/api/base')
DATELIST = []


@mt_base.route('/getdate', methods=['GET'])
def get_date():
    res = db.session.query(models.DateTime).all()
    status = 0 if res else 1
    index = 0
    while 1:
        if len(DATELIST) == len(res):
            break
        for i in res:
            if i.PreviousId == index:
                DATELIST.append(i)
                index = i.id
    msg = "未设置时间" if status else [{'id': item.id,
                                   'previousid': item.PreviousId,
                                   'startTime': item.startTime,
                                   'endTime': item.endTime} for item in DATELIST]
    db.session.remove()
    return jsonify(
        status=0,
        message=msg
    )


@mt_base.route('/add-date', methods=['POST'])
def add_date():
    data = json.loads(request.get_data(as_text=True))

    res = db.session.query(models.DateTime).all()
    PreviousId = DATELIST[-1] if res else 0
    db.session.add(models.DateTime(endTime=data.get('endTime'),
                                   startTime=data.get('startTime'),
                                   PreviousId=PreviousId))
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='添加成功'
    )


@mt_base.route('/update-date', methods=['POST'])
def update_date():
    data = json.loads(request.get_data(as_text=True))
    db.session.query(models.DateTime).filter(models.DateTime.id == data.get('id')).update(
        {'endTime': data.get('endTime'),
         'startTime': data.get('startTime')})
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='修改成功'
    )


@mt_base.route('/del-date/<int:uid>', methods=['GET'])
def del_date(uid):
    res = db.session.query(models.DateTime.id, models.DateTime.PreviousId).filter(models.DateTime.id == uid).first()
    if res:
        id, pid = res.id, res.PreviousId
        db.session.query(models.DateTime).filter(models.DateTime.PreviousId == id).update({'PreviousId': pid})
        db.session.query(models.DateTime).filter(models.DateTime.id == uid).delete()
    else:
        db.session.query(models.DateTime).filter(models.DateTime.id == uid).delete()
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='删除成功'
    )


@mt_base.route('/insert-date', methods=['POST'])
def insert_date():
    data = json.loads(request.get_data(as_text=True))
    date = models.DateTime(PreviousId=data.get('previousid'),
                           startTime=data.get('startTime'),
                           endTime=data.get('endTime'))
    db.session.add(date)
    db.session.flush()
    db.session.query(models.DateTime).filter(models.DateTime.id == data.get('id')).update({"PreviousId": date.id})
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='插入成功'
    )


@mt_base.route('/menus', methods=['POST'])
def post_menus():
    # username = session.get('username')
    # print('base:', username)
    data = json.loads(request.get_data(as_text=True))
    username = data.get('username')
    menu = db.session.query(models.User.menu).filter(models.User.username == username).first()
    res = db.session.query(models.Menus).filter(models.Menus.id.in_([int(i) for i in menu[0].split(',')])).all()
    msg = [{'id': item.id, 'menuname': item.menuname} for item in res]
    db.session.remove()
    return jsonify(
        status=0,
        message=msg
    )


@mt_base.route('/getmenus', methods=['GET'])
def get_menus():
    res = db.session.query(models.Menus.id, models.Menus.menuname).all()
    db.session.remove()
    return jsonify(
        status=0,
        message=[{'id': item.id, 'menuname': item.menuname} for item in res]
    )


@mt_base.route('/getdepart', methods=['GET'])
def get_depart():
    res = db.session.query(models.Depart).all()
    db.session.remove()
    return jsonify(
        status=0,
        message=[{
            'id': item.id,
            'departname': item.departname
        } for item in res]
    )


@mt_base.route('/add-depart', methods=['POST'])
def add_depart():
    data = json.loads(request.get_data(as_text=True))
    db.session.add(models.Depart(departname=data.get('departname')))
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='添加成功'
    )


@mt_base.route('/update-depart', methods=['POST'])
def update_depart():
    data = json.loads(request.get_data(as_text=True))
    db.session.query(models.Depart).filter(models.Depart.id == data.get('id')).update(
        {'departname': data.get('departname')})
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='更新成功'
    )


@mt_base.route('/del-depart/<int:uid>', methods=['GET'])
def del_depart(uid):
    res = db.session.query(models.User.username).filter(models.User.departId == int(uid)).first()
    if res.username:
        status = 1
        msg = '部门被使用，不能删除'
    else:
        db.session.query(models.Depart).filter(models.Depart.id == int(uid)).delete()
        db.session.commit()
        status = 0
        msg = '删除成功'
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_base.route('/level', methods=['GET'])
def get_room_level():
    res = db.session.query(models.RoomLevel).all()
    db.session.remove()
    return jsonify(
        status=0,
        message=sorted([{'id': item.id, 'level': item.level} for item in res], key=lambda x: x.get('id'))
    )
