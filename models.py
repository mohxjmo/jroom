# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 14:57
# @Author  : huxiajie
from extensions import db


class User(db.Model):
    __tablename__ = 'user'
    usertel = db.Column(db.String(11), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    userpsw = db.Column(db.String(10), nullable=False)
    usersex = db.Column(db.Boolean, nullable=False)
    useremail = db.Column(db.String(30))
    useravatar = db.Column(db.String(100))
    userjob = db.Column(db.String(20))
    # relationship
    userrecord = db.relationship('Userrecord', backref=db.backref("user"))
    rentrecord = db.relationship('Rentrecord', backref=db.backref("user"))


class Manager(db.Model):
    __tablename__ = 'manager'
    mantel = db.Column(db.String(11), primary_key=True, nullable=False)
    manname = db.Column(db.String(10), nullable=False)
    manpsw = db.Column(db.String(10), nullable=False)


class House(db.Model):
    __tablename__ = 'house'
    houseID = db.Column(db.String(20), primary_key=True)
    housetitle = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(10), nullable=False)
    district = db.Column(db.String(10), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    community = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(10), nullable=False)
    lng = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.String(30), nullable=False)
    housepic = db.Column(db.String(200), nullable=False)
    housearea = db.Column(db.Float, nullable=False)
    housedirect = db.Column(db.String(5), nullable=False)
    housefloor = db.Column(db.String(5), nullable=False)
    househall = db.Column(db.String(10), nullable=False)
    balcony = db.Column(db.Boolean, nullable=False)
    bathroom = db.Column(db.Boolean, nullable=False)
    housestatus = db.Column(db.Boolean, nullable=False)
    housetype = db.Column(db.String(5), nullable=False)
    housearound = db.Column(db.Text)
    # 外码
    tenanttel = db.Column(db.String(11), db.ForeignKey('user.usertel'))
    # relationship
    tenant = db.relationship('User', backref=db.backref('renthouse'))
    pics = db.relationship('Housepic', backref=db.backref('house'))
    prices = db.relationship('Payment', backref=db.backref('house'))


class Housepic(db.Model):
    __tablename__ = 'housepic'
    picID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pic = db.Column(db.String(200), nullable=False)
    # 外码
    houseID = db.Column(db.String(20), db.ForeignKey('house.houseID'), nullable=False)


class Payment(db.Model):
    __tablename__ = 'payment'
    payID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payname = db.Column(db.String(10), nullable=False)
    payrent = db.Column(db.Integer, nullable=False)
    paydeposit = db.Column(db.Integer, nullable=False)
    payservice = db.Column(db.Integer, nullable=False)
    # 外码
    houseID = db.Column(db.String(20), db.ForeignKey('house.houseID'), nullable=False)


class Userrecord(db.Model):
    __tablename__ = 'userrecord'
    ureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 看房 收藏房 售后
    uretype = db.Column(db.String(10), nullable=False)
    timeapply = db.Column(db.Date)
    timedeal = db.Column(db.Date)
    timeend = db.Column(db.Date)
    urestatus = db.Column(db.String(10), nullable=False)
    # 外码
    usertel = db.Column(db.String(11), db.ForeignKey('user.usertel'), nullable=False)
    houseID = db.Column(db.String(20), db.ForeignKey('house.houseID'), nullable=False)


class Rentrecord(db.Model):
    __tablename__ = 'rentrecord'
    reID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    retime = db.Column(db.Date, nullable=False)
    repayment = db.Column(db.String(10), nullable=False)
    rerent = db.Column(db.Integer, nullable=False)
    redeposit = db.Column(db.Integer, nullable=False)
    reservice = db.Column(db.Integer, nullable=False)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    # 外码
    usertel = db.Column(db.String(11), db.ForeignKey('user.usertel'), nullable=False)
    houseID = db.Column(db.String(20), db.ForeignKey('house.houseID'), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    community = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    tel = db.Column(db.String(11), nullable=False)