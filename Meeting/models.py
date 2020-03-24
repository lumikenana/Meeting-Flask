from Meeting import db

"""
会议室预定系统：
    User：
        userid PK
        username not Null
        telephone
        email
        departid FK
    Depart:
        departid PK
        departname not null
    MeetingRoom:
        roomid PK
        roomname UK + not Null
        level NN
    BookedMeetingRoom
        id PK
        bookerid FK
        roomid FK
        booktime not Null  :
            {
                1~5： 周一~周五
            }
            {
                1: 9-10
                2: 10-11
                3: 11-12
                4: 12-13
                5: 13-14
                6: 14-15
                7: 15-16
                8: 16-17
                9: 17-18
            }
            以eg: 1_1/1_3...方式拼接
"""


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30))
    telephone = db.Column(db.String(20))
    menu = db.Column(db.String(20))

    departId = db.Column(db.Integer, db.ForeignKey('depart.id'))
    depart = db.relationship('Depart', backref='user')


class Depart(db.Model):
    __tablename__ = 'depart'
    id = db.Column(db.Integer, primary_key=True)
    departname = db.Column(db.String(50), nullable=False)


class MeetingRoom(db.Model):
    __tablename__ = 'meetingroom'
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)


class DateTime(db.Model):
    __tablename__ = 'datetime'
    id = db.Column(db.Integer, primary_key=True)
    PreviousId = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.String(20), nullable=False)
    endTime = db.Column(db.String(20), nullable=False)


class BookedRoom(db.Model):
    __tablename__ = 'bookedroom'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='bookedroom')

    roomId = db.Column(db.Integer, db.ForeignKey('meetingroom.id'))
    meetingRoom = db.relationship('MeetingRoom', backref='bookedroom')

    bookDate = db.Column(db.String(20), nullable=False)
    timeId = db.Column(db.Integer, nullable=False)


class Menus(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    menuname = db.Column(db.String(50), nullable=False)


class RoomLevel(db.Model):
    __tablename__ = 'roomlevel'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10), nullable=False, unique=True)
