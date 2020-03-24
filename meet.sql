create table depart (
	departid int auto_increment,
    departname varchar(30) not null
);

create table users (
	userid int auto_increment,
    username varchar(30) not null,
    telephone varchar(20),
    email varchar(50),
	departid int not null,
    foreign key(departid) references depart(departid)
);

create table meetingroom (
	roomid int auto_increment,
    roomname varchar(30) unique not null,
    level int not null
);

create table bookedmeetingroom (
	id int auto_increment,
    bookerid int not null,
    roomid int not null,
    booktime varchar(10) not null,
    foreign key(bookerid) references users(userid),
    foreign key(roomid) references meetingroom(roomid)
);

