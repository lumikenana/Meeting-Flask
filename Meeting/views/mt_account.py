import base64
import random
import time

from flask import Blueprint, jsonify, request, session
import json
from Meeting import models, db

mt_account = Blueprint("account", __name__, url_prefix='/api/account')


def gen_token(uid):
    token = base64.b64encode(":".join([str(uid), str(random.random()), str(time.time() + 7200)]))
    return token


def verify_token(token):
    _token = base64.b64decode(token)
    return _token


@mt_account.route('/postuserinfo', methods=['POST'])
def postuserinfo():
    msg = {}
    data = json.loads(request.get_data(as_text=True))
    res = db.session.query(models.User.username, models.User.password).filter(
        models.User.username == data['username'] and models.User.password == data['password']).first()
    if res:
        if res.username == data['username'] and res.password == data['password']:
            status, msg['err'], msg['token'] = 0, '', res.username
            session['username'] = res.username
        else:
            status, msg['err'] = 1, '密码错误'
    else:
        status, msg['err'] = 2, '用户名不存在'
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_account.route('/users', methods=['GET'])
def get_users():
    res = db.session.query(models.User.id, models.User.username, models.User.email, models.User.telephone,
                           models.User.menu, models.User.departId, models.Depart.departname).join(models.Depart).all()
    menu = db.session.query(models.Menus.id, models.Menus.menuname).all()
    menus = {}
    for a in menu:
        menus[a.id] = a.menuname
    msg = [{'id': item.id,
            'username': item.username,
            'email': item.email,
            'telephone': item.telephone,
            'depart': item.departId,
            'departname': item.departname,
            'menus': [int(i) for i in item.menu.split(',')],
            'strmenu': '，'.join(sorted([menus.get(j) for j in map(int, item.menu.split(','))]))} for item in res]
    db.session.remove()
    return jsonify(
        status=0,
        message=msg
    )


@mt_account.route('/del-user/<int:uid>', methods=['GET'])
def del_user(uid):
    try:
        db.session.query(models.User).filter(models.User.id == uid).delete()
        db.session.commit()
        status, msg = 0, '删除成功'
    except Exception as e:
        status, msg = 1, str(e)
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_account.route('/add-user', methods=['POST'])
def add_user():
    default_pwd = '12345678'
    try:
        data = json.loads(request.get_data(as_text=True))
        db.session.add(models.User(username=str(data.get('username')),
                                   password=default_pwd,
                                   email=str(data.get('email')),
                                   telephone=str(data.get('telephone')),
                                   departId=int(data.get('depart')),
                                   menu=','.join(map(str, data.get('menus')))
                                   ))
        db.session.commit()
        status, msg = 0, '添加成功'
    except Exception as e:
        status, msg = 1, str(e)
    db.session.remove()
    return jsonify(
        status=status,
        message=msg
    )


@mt_account.route('/update-user', methods=['POST'])
def update_user():
    data = json.loads(request.get_data(as_text=True))
    db.session.query(models.User).filter(models.User.id == data.get('id')).update({'username': data.get('username'),
                                                                                   'email': data.get('email'),
                                                                                   'telephone': data.get('telephone'),
                                                                                   'departId': data.get('depart'),
                                                                                   'menu': ','.join(
                                                                                       map(str, data.get('menus'))),
                                                                                   })
    db.session.commit()
    db.session.remove()
    return jsonify(
        status=0,
        message='更新成功'
    )
