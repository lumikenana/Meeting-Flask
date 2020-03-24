from flask.blueprints import Blueprint
from flask import jsonify, request
from Meeting import db
from Meeting import models
import json

mt_room = Blueprint('mt_room', __name__, url_prefix='/api/room')


@mt_room.route('/getroom', methods=['GET'])
def get_room():
    res = db.session.query(models.MeetingRoom, models.RoomLevel).filter(
        models.MeetingRoom.level == models.RoomLevel.id).all()
    msg = [{'roomid': item[0].id, 'roomname': item[0].roomname, 'levelid': item[0].level, 'level': item[1].level} for
           item in res]
    db.session.remove()
    return jsonify(
        status=0,
        message=msg
    )


@mt_room.route('/add-room', methods=['POST'])
def add_room():
    data = json.loads(request.get_data(as_text=True))
    db.session.add(models.MeetingRoom(roomname=data.get('roomname'), level=data.get('level')))
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='添加成功'
    )


@mt_room.route('update-room', methods=['POST'])
def update_room():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    db.session.query(models.MeetingRoom).filter(models.MeetingRoom.id == data.get('roomid')).update(
        {'roomname': data.get('roomname'), 'level': data.get('levelid')})
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='修改成功'
    )


@mt_room.route('/del-room/<int:uid>', methods=['GET'])
def del_room(uid):
    db.session.query(models.MeetingRoom).filter(models.MeetingRoom.id == int(uid)).delete()
    db.session.commit()
    status = 0
    msg = '删除成功'

    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_room.route('/booked-room', methods=['POST'])
def book_room():
    data = json.loads(request.get_data(as_text=True))
    res = db.session.query(models.BookedRoom).filter(models.BookedRoom.roomId == data.get('roomId'),
                                                     models.BookedRoom.bookDate == data.get('date'),
                                                     models.BookedRoom.timeId == data.get('timeId')).first()
    if res:
        status = 1
        msg = '已被预订'
    else:
        uid = db.session.query(models.User.id).filter(models.User.username == data.get('userName')).first()
        Booked = models.BookedRoom(userId=uid.id,
                                   roomId=data.get('roomId'),
                                   bookDate=data.get('date'),
                                   timeId=data.get('timeId'))
        db.session.add(Booked)
        status, msg = 0, '预定成功'
        db.session.commit()
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_room.route('/getbooked-room/<int:id>', methods=['GET'])
def booked_room(id):
    res = db.session.query(models.BookedRoom, models.User.username, models.DateTime).filter(
        models.BookedRoom.roomId == id, models.BookedRoom.timeId == models.DateTime.id).join(models.User).all()
    msg = [{
        'id': item[0].id,
        'userid': item[0].userId,
        'username': item[1],
        'roomid': item[0].roomId,
        'bookDate': item[0].bookDate,
        'timeid': item[0].timeId,
        'startTime': item[2].startTime,
        'endTime': item[2].endTime
    } for item in res]
    status = 0
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_room.route('/cancel_book', methods=['POST'])
def cancel_book():
    data = json.loads(request.get_data(as_text=True))
    db.session.query(models.BookedRoom).filter(models.BookedRoom.timeId == data.get('timeid'),
                                               models.BookedRoom.bookDate == data.get('date')).delete()
    db.session.commit()
    db.session.remove()
    return jsonify()
