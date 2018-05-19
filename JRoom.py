# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 9:44
# @Author  : huxiajie
from flask import Flask, render_template, request, jsonify, json, session, redirect, url_for
import config
from extensions import db
from models import House, Housepic, Payment, User, Manager, Userrecord, Rentrecord, Post
import sys
from datetime import date

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def cover():
    return render_template('cover.html')


@app.route('/map', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        districtCount = {"东城": 0, "西城": 0, "朝阳": 0, "丰台": 0, "石景山": 0, "海淀": 0, "门头沟": 0, "房山": 0, "通州": 0, "顺义": 0,
                         "昌平": 0, "大兴": 0, "亦庄开发": 0}
        districtCount["东城"] = House.query.filter(House.district == '东城').count()
        districtCount["西城"] = House.query.filter(House.district == '西城').count()
        districtCount["朝阳"] = House.query.filter(House.district == '朝阳').count()
        districtCount["丰台"] = House.query.filter(House.district == '丰台').count()
        districtCount["石景山"] = House.query.filter(House.district == '石景山').count()
        districtCount["海淀"] = House.query.filter(House.district == '海淀').count()
        districtCount["门头沟"] = House.query.filter(House.district == '门头沟').count()
        districtCount["房山"] = House.query.filter(House.district == '房山').count()
        districtCount["通州"] = House.query.filter(House.district == '通州').count()
        districtCount["顺义"] = House.query.filter(House.district == '顺义').count()
        districtCount["昌平"] = House.query.filter(House.district == '昌平').count()
        districtCount["大兴"] = House.query.filter(House.district == '大兴').count()
        districtCount["亦庄开发"] = House.query.filter(House.district == '亦庄开发').count()
        areaCount = {}
        communityCount = {}
        houses = House.query.filter(House.housestatus == 1).all()
        for house in houses:
            if house.area in areaCount.keys():
                areaCount[house.area] += 1
            else:
                areaCount[house.area] = 1

            if house.community in communityCount.keys():
                communityCount[house.community]['num'] += 1
            else:
                communityCount[house.community] = {'community': house.community,
                                                   'num': 1,
                                                   'lng': house.lng,
                                                   'lat': house.lat}
        luxhouses = Payment.query.filter(Payment.payname == '月付').order_by('-payrent').all()
        count = 200
        lux = []
        for luxhouse in luxhouses:
            if count == 0:
                break
            lux.append({
                'houseID': luxhouse.house.houseID,
                'title': luxhouse.house.housetitle,
                'hall': luxhouse.house.househall,
                'area': luxhouse.house.housearea,
                'floor': luxhouse.house.housefloor,
                'pic': luxhouse.house.housepic,
                'price': luxhouse.payrent,
                'priceunit': luxhouse.payname,
                'type': luxhouse.house.housetype
            })
            count -= 1
        data = {
            'districtCount': districtCount,
            'areaCount': areaCount,
            'communityCount': communityCount,
            'expensives': lux
        }
        return render_template('index.html', **data)
    else:
        houseList = []
        count = 400
        type = request.form.get('type')
        renttype = request.form.get('renttype')
        if renttype == u"出租方式":
            renttype = "%%"
        minprice = int(request.form.get('price').split()[0])
        if minprice == 0:
            minprice = -1
        maxprice = int(request.form.get('price').split()[1])
        if maxprice == 0:
            maxprice = sys.maxint
        minarea = float(request.form.get('area').split()[0])
        if minarea == 0:
            minarea = -1.00
        maxarea = float(request.form.get('area').split()[1])
        if maxarea == 0:
            maxarea = float(sys.maxint)
        direct = request.form.get('direct')
        if direct == u"朝向":
            direct = "%%"
        else:
            direct = "%" + direct + "%"
        bathroom = request.form.get('bathroom')
        balcony = request.form.get('balcony')
        if bathroom == '0':
            bathroom = [0, 1]
        else:
            bathroom = [1]
        if balcony == '0':
            balcony = [0, 1]
        else:
            balcony = [1]
        # important: 控制台输出中文 print json.dumps(renttype).decode("unicode-escape")
        if type == 'click_community':
            print('*********' + type + '*********')
            community = request.form.get('community')
            community = community.split()[0]
            houses = House.query.filter(House.community == community, House.housestatus == 1,
                                        House.housetype.like(renttype),
                                        House.housearea >= minarea, House.housearea <= maxarea,
                                        House.housedirect.like(direct), House.bathroom.in_(bathroom),
                                        House.balcony.in_(balcony)).all()
            for house in houses:
                if house.prices[0].payrent >= minprice and house.prices[0].payrent <= maxprice:
                    houseList.append({
                        'houseID': house.houseID,
                        'title': house.housetitle,
                        'hall': house.househall,
                        'area': house.housearea,
                        'floor': house.housefloor,
                        'pic': house.housepic,
                        'price': house.prices[0].payrent,
                        'priceunit': house.prices[0].payname,
                        'type': house.housetype
                    })
            return jsonify(houseList)
        if type == 'view_district':
            print('*********' + type + '*********')
            districts = request.form.getlist('districts[]')
            if len(districts) == 0:
                return jsonify(houseList)
            for district in districts:
                houses = House.query.filter(House.district == district, House.housestatus == 1,
                                            House.housetype.like(renttype),
                                            House.housearea >= minarea, House.housearea <= maxarea,
                                            House.housedirect.like(direct),
                                            House.bathroom.in_(bathroom), House.balcony.in_(balcony)).all()
                for house in houses:
                    if count == 0:
                        break
                    if house.prices[0].payrent >= minprice and house.prices[0].payrent <= maxprice:
                        houseList.append({
                            'houseID': house.houseID,
                            'title': house.housetitle,
                            'hall': house.househall,
                            'area': house.housearea,
                            'floor': house.housefloor,
                            'pic': house.housepic,
                            'price': house.prices[0].payrent,
                            'priceunit': house.prices[0].payname,
                            'type': house.housetype
                        })
                        count -= 1
                if count == 0:
                    break
            return jsonify(houseList)
        if type == 'view_area':
            print('*********' + type + '*********')
            areas = request.form.getlist('areas[]')
            if len(areas) == 0:
                return jsonify(houseList)
            for area in areas:
                houses = House.query.filter(House.area == area, House.housestatus == 1, House.housetype.like(renttype),
                                            House.housearea >= minarea, House.housearea <= maxarea,
                                            House.housedirect.like(direct),
                                            House.bathroom.in_(bathroom), House.balcony.in_(balcony)).all()
                for house in houses:
                    if count == 0:
                        break
                    if house.prices[0].payrent >= minprice and house.prices[0].payrent <= maxprice:
                        houseList.append({
                            'houseID': house.houseID,
                            'title': house.housetitle,
                            'hall': house.househall,
                            'area': house.housearea,
                            'floor': house.housefloor,
                            'pic': house.housepic,
                            'price': house.prices[0].payrent,
                            'priceunit': house.prices[0].payname,
                            'type': house.housetype
                        })
                        count -= 1
                if count == 0:
                    break
            return jsonify(houseList)
        if type == 'view_community':
            print('*********' + type + '*********')
            communities = request.form.getlist('communities[]')
            if len(communities) == 0:
                return jsonify(houseList)
            for comm in communities:
                houses = House.query.filter(House.community == comm, House.housestatus == 1,
                                            House.housetype.like(renttype),
                                            House.housearea >= minarea, House.housearea <= maxarea,
                                            House.housedirect.like(direct),
                                            House.bathroom.in_(bathroom), House.balcony.in_(balcony)).all()
                for house in houses:
                    if count == 0:
                        break
                    if house.prices[0].payrent >= minprice and house.prices[0].payrent <= maxprice:
                        houseList.append({
                            'houseID': house.houseID,
                            'title': house.housetitle,
                            'hall': house.househall,
                            'area': house.housearea,
                            'floor': house.housefloor,
                            'pic': house.housepic,
                            'price': house.prices[0].payrent,
                            'priceunit': house.prices[0].payname,
                            'type': house.housetype
                        })
                        count -= 1
                if count == 0:
                    break
            return jsonify(houseList)


@app.route('/detail/<houseid>', methods=['GET', 'POST'])
def detail(houseid):
    if request.method == 'GET':
        id = json.dumps(houseid).replace("\"", "")
        house = House.query.filter(House.houseID == id).first()
        return render_template('detail.html', house=house)
    if request.method == 'POST':
        type = request.form.get('type')
        if type == 'yykf':
            if session.get('usertel'):
                record = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                                 Userrecord.houseID == houseid, Userrecord.uretype == '预约看房').order_by(
                    '-timeapply').first()
                # 从未约看该房源, 添加新的约看记录
                if record is None:
                    re = Userrecord(uretype='预约看房', timeapply=date.today(), urestatus='已约看',
                                    usertel=session.get('usertel'), houseID=houseid)
                    db.session.add(re)
                    db.session.commit()
                    return jsonify('ok')
                # 已取消上次约看, 更改约看记录
                elif record.urestatus == u"已取消约看":
                    record.urestatus = "已约看"
                    record.timeapply = date.today()
                    db.session.commit()
                    return jsonify("ok")
                # 已完成上次约看(urestatus为已完成约看), 添加新的约看记录（距上次约看结束至少相隔一周）
                else:
                    today = date.today()
                    if (today - record.timeend).days() <= 7:
                        return jsonify("toosoon")
                    else:
                        re = Userrecord(uretype='预约看房', timeapply=date.today(), urestatus='已约看',
                                        usertel=session.get('usertel'), houseID=houseid)
                        db.session.add(re)
                        db.session.commit()
                        return jsonify('ok')
            else:
                return jsonify("nologin")
        if type == 'noyykf':
            record = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                             Userrecord.houseID == houseid,
                                             Userrecord.uretype == '预约看房').order_by('-timeapply').first()
            record.urestatus = "已取消约看"
            db.session.commit()
            return jsonify("ok")
        if type == 'scfy':
            if session.get('usertel'):
                record = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                                 Userrecord.houseID == houseid, Userrecord.uretype == '收藏房源').first()
                # 从未收藏该房源
                if record is None:
                    re = Userrecord(uretype='收藏房源', urestatus='已收藏', timeapply=date.today(),
                                    usertel=session.get('usertel'), houseID=houseid)
                    db.session.add(re)
                    db.session.commit()
                    return jsonify('ok')
                # 再次收藏
                else:
                    record.urestatus = '已收藏'
                    record.timeapply = date.today()
                    db.session.commit()
                    return jsonify('ok')
            else:
                return jsonify("nologin")
        if type == "noscfy":
            record = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                             Userrecord.houseID == houseid, Userrecord.uretype == '收藏房源').first()
            # 取消收藏
            record.urestatus = '已取消'
            db.session.commit()
            return jsonify('ok')
        if type == 'btn':
            if session.get('usertel'):
                # no : 未收藏、未约看
                data = {}
                # 已出租
                status = House.query.filter(House.houseID == houseid, House.housestatus == 1).first()
                if status is None:
                    return jsonify('unrentable')
                # 未出租
                yykf = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                               Userrecord.houseID == houseid,
                                               Userrecord.uretype == '预约看房').order_by('-timeapply').first()
                if yykf is None:
                    data["yykf"] = "no"
                elif yykf.urestatus == u"已结束":
                    data["yykf"] = "no"
                else:
                    data["yykf"] = "yes"
                scfy = Userrecord.query.filter(Userrecord.usertel == session.get('usertel'),
                                               Userrecord.houseID == houseid,
                                               Userrecord.uretype == '收藏房源').first()
                if scfy is None:
                    data["scfy"] = "no"
                elif scfy.urestatus == u"已收藏":
                    data["scfy"] = "yes"
                else:
                    data["scfy"] = "no"
                return jsonify(data)
            else:
                return jsonify("nologin")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usertel = request.form.get('usertel')
        userpsw = request.form.get('userpsw')
        user = User.query.filter(User.usertel == usertel, User.userpsw == userpsw).first()
        if user:
            session['usertel'] = user.usertel
            session['username'] = user.username
            # 31天内不重复登录
            session.permanent = True
            return jsonify(True)
        return jsonify(False)


@app.route('/logout', methods=['POST'])
def logout():
    session['usertel'] = None
    session['username'] = None
    return jsonify(True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        type = request.form.get("type")
        if type == "usertel":
            tel = request.form.get("usertel")
            isRegister = User.query.filter(User.usertel == tel).count()
            if isRegister == 0:
                return jsonify(True)
            else:
                return jsonify(False)
        if type == "register":
            if request.form.get('usersex') == "0":
                sex = 0
            else:
                sex = 1
            user = User(usertel=request.form.get('usertel'), username=request.form.get('username'),
                        userpsw=request.form.get('userpsw'), usersex=sex,
                        useremail=request.form.get('useremail'), userjob=request.form.get('userjob'), useravatar="")
            db.session.add(user)
            db.session.commit()
            session['usertel'] = user.usertel
            session['username'] = user.username
            session.permanent = True  # 31天内不重复登录
            return jsonify('success')


@app.route('/user/<menu>', methods=['GET', 'POST'])
def user(menu):
    if request.method == 'GET':
        if menu == 'info':
            user = User.query.filter(User.usertel == session['usertel']).first()
            if user.useravatar is None:
                user.useravatar = ""
            if user.useremail is None or user.useremail == "":
                user.useremail = u"未绑定"
            if user.userjob is None or user.userjob == "":
                user.userjob = u"未填写"
            return render_template('userinfo.html', user=user)
        if menu == 'likes':
            page = int(request.args.get('page'))
            pagination = Userrecord.query.filter(Userrecord.usertel == session['usertel'], Userrecord.uretype == '收藏房源',
                                                 Userrecord.urestatus == '已收藏').order_by('-timeapply').paginate(
                page=page, per_page=5, max_per_page=5, error_out=False)
            if pagination.total == 0:
                return render_template('userlikes.html', flag="no")
            else:
                houses = []
                for item in pagination.items:
                    house = House.query.filter(House.houseID == item.houseID).first()
                    house = {
                        'id': house.houseID,
                        'pic': house.housepic,
                        'title': house.housetitle,
                        'status': house.housestatus,
                        'time': item.timeapply
                    }
                    houses.append(house)
                return render_template('userlikes.html', flag="yes", pagination=pagination, houses=houses)
        if menu == 'views':
            page = int(request.args.get('page'))
            status = request.args.get('status')
            if status == 'ing':
                pagination = Userrecord.query.filter(Userrecord.usertel == session['usertel'],
                                                     Userrecord.uretype == '预约看房',
                                                     Userrecord.urestatus == '已约看').order_by('-timeapply').paginate(
                    page=page, per_page=5, max_per_page=5, error_out=False)
                if pagination.total == 0:
                    return render_template('userviewsING.html', flag="no")
                else:
                    houses = []
                    for item in pagination.items:
                        house = House.query.filter(House.houseID == item.houseID).first()
                        house = {
                            'id': house.houseID,
                            'pic': house.housepic,
                            'title': house.housetitle,
                            'status': house.housestatus,
                            'time': item.timeapply
                        }
                        houses.append(house)
                    return render_template('userviewsING.html', flag="yes", pagination=pagination, houses=houses)
            if status == 'end':
                pagination = Userrecord.query.filter(Userrecord.usertel == session['usertel'],
                                                     Userrecord.uretype == '预约看房',
                                                     Userrecord.urestatus == '已完成约看').order_by('-timeend').paginate(
                    page=page, per_page=5, max_per_page=5, error_out=False)
                if pagination.total == 0:
                    return render_template('userviewsEND.html', flag="no")
                else:
                    houses = []
                    for item in pagination.items:
                        house = House.query.filter(House.houseID == item.houseID).first()
                        house = {
                            'id': house.houseID,
                            'pic': house.housepic,
                            'title': house.housetitle,
                            'status': house.housestatus,
                            'timeapply': item.timeapply,
                            'timeend': item.timeend
                        }
                        houses.append(house)
                    return render_template('userviewsEND.html', flag="yes", pagination=pagination, houses=houses)
        if menu == 'rents':
            page = int(request.args.get('page'))
            pagination = Rentrecord.query.filter(Rentrecord.usertel == session['usertel']).order_by('-retime').paginate(
                page=page, per_page=5, max_per_page=5, error_out=False)
            if pagination.total == 0:
                return render_template('userrents.html', flag="no")
            else:
                houses = []
                for item in pagination.items:
                    house = House.query.filter(House.houseID == item.houseID).first()
                    if item.checkout < date.today():
                        status = u'已结束'
                    else:
                        status = u'进行中'
                    house = {
                        'id': house.houseID,
                        'pic': house.housepic,
                        'title': house.housetitle,
                        'checkin': item.checkin,
                        'checkout': item.checkout,
                        'rent': item.rerent,
                        'payment': item.repayment,
                        'deposit': item.redeposit,
                        'service': item.reservice,
                        'status': status
                    }
                    houses.append(house)
                return render_template('userrents.html', flag="yes", pagination=pagination, houses=houses)
    else:
        if menu == 'info':
            user = User.query.filter(User.usertel == session['usertel']).first()
            type = request.form.get('type')
            data = {}
            if type == "info":
                name = request.form.get('name')
                email = request.form.get('email')
                job = request.form.get('job')
                user.username = name
                user.useremail = email
                user.userjob = job
                db.session.commit()
                data["name"] = name
                if email == "":
                    data["email"] = "未绑定"
                else:
                    data["email"] = email
                if job == "":
                    data["job"] = "未填写"
                else:
                    data["job"] = job
                session['username'] = name
                return jsonify(data)
            if type == "psw":
                user.userpsw = request.form.get('psw')
                db.session.commit()
                return jsonify("ok")
            if type == "avatar":
                pass
            if type == "cancel":
                user = User.query.filter(User.usertel == session['usertel']).first()
                data = {}
                data["name"] = user.username
                if user.useremail is None or user.useremail == "":
                    data["email"] = u"未绑定"
                else:
                    data["email"] = user.useremail
                if user.userjob is None or user.userjob == "":
                    data["job"] = u"未填写"
                else:
                    data["job"] = user.userjob
                return jsonify(data)
        if menu == 'likes':
            houseid = request.form.get('houseid')
            re = Userrecord.query.filter(Userrecord.houseID == houseid, Userrecord.usertel == session['usertel'],
                                         Userrecord.uretype == '收藏房源').first()
            re.urestatus = '已取消'
            db.session.commit()
            return 'ok'
        if menu == 'views':
            houseid = request.form.get('houseid')
            re = Userrecord.query.filter(Userrecord.houseID == houseid, Userrecord.usertel == session['usertel'],
                                         Userrecord.uretype == '预约看房', Userrecord.urestatus == '已约看').first()
            re.urestatus = '已取消约看'
            db.session.commit()
            return 'ok'


@app.route('/posthouse', methods=['GET', 'POST'])
def posthouse():
    if request.method == 'GET':
        return render_template('postHouse.html')
    else:
        posthouse = Post(district=request.form.get('district'), street=request.form.get('street'),
                         community=request.form.get('community'),
                         price=int(request.form.get('price')), tel=request.form.get('tel'),status='已委托')
        db.session.add(posthouse)
        db.session.commit()
        return jsonify('success')


@app.route('/admin/<menu>',methods=['GET','POST'])
def admin(menu):
    if request.method == 'GET':
        if menu == 'login':
            return render_template('admin/adminLogin.html')
        if menu == 'admin':
            return render_template('admin/admin.html')
        if menu == 'post1':
            page = int(request.args.get('page'))
            pagination = Post.query.order_by('-ID').paginate(
                page=page, per_page=10, max_per_page=10, error_out=False)
            if pagination.total == 0:
                return render_template('admin/adminPost1.html', flag="no")
            else:
                posts = []
                for item in pagination.items:
                    # status: 已委托 待审核 已发布
                    if item.status == u'已发布':
                        pass
                    else:
                        posts.append(item)
                return render_template('admin/adminPost1.html', flag="yes", pagination=pagination, posts=posts)
        if menu == 'post2':
            return render_template('admin/adminPost2.html')
        if menu == 'view':
            # status： 已约看 已取消约看 已完成约看
            page = int(request.args.get('page'))
            pagination = Userrecord.query.filter(Userrecord.uretype == '预约看房', Userrecord.urestatus != '已取消约看').order_by('-timeapply').paginate(page=page, per_page=10, max_per_page=10, error_out=False)
            if pagination.total == 0:
                return render_template('admin/adminView.html', flag="no")
            else:
                views = []
                for item in pagination.items:
                    views.append(item)
                return render_template('admin/adminView.html', flag="yes", pagination=pagination, views=views)
        if menu == 'rent1':
            page = int(request.args.get('page'))
            pagination = Rentrecord.query.order_by('-retime').paginate(page=page, per_page=10, max_per_page=10, error_out=False)
            if pagination.total == 0:
                return render_template('admin/adminRent1.html', flag="no")
            else:
                rents = []
                for item in pagination.items:
                    rents.append(item)
                return render_template('admin/adminRent1.html',rents=rents,flag="yes", pagination=pagination)
        if menu == 'rent2':
            return render_template('admin/adminRent2.html')
        if menu == 'info':
            return render_template('admin/adminInfo.html')
    else:
        if menu == 'login':
            mantel = request.form.get('usertel')
            manpsw = request.form.get('userpsw')
            manager = Manager.query.filter(Manager.mantel == mantel, Manager.manpsw == manpsw).first()
            if manager:
                session['mantel'] = mantel
                session['manpsw'] = manpsw
                session['manname'] = manager.manname
                # 31天内不重复登录
                session.permanent = True
                return jsonify(True)
            return jsonify(False)
        if menu == 'post1':
            type = request.form.get('type')
            if type=='check':
                pid = request.form.get('pid')
                post = Post.query.filter(Post.ID == pid).first()
                post.status = '待审核'
                db.session.commit()
                return 'success'
            if type=='post':
                pass
            if type=='delete':
                pid = request.form.get('pid')
                post = Post.query.filter(Post.ID == pid).first()
                db.session.delete(post)
                db.session.commit()
                return 'success'
            return render_template('admin/adminPost1.html')
        if menu == 'post2':
            type = request.form.get('type')
            if type=='checkpid':
                pid = request.form.get('pid')
                post = Post.query.filter(Post.ID == pid, Post.status=='待审核').first()
                data = {}
                if post:
                    data['district'] = post.district
                    data['street'] = post.street
                    data['community'] = post.community
                    return jsonify(data)
                else:
                    return jsonify('nodata')
        if menu == 'view':
            type = request.form.get('type')
            if type == 'timedeal':
                record = Userrecord.query.filter(Userrecord.ureID == request.form.get('id')).first()
                record.timedeal = request.form.get('timedeal')
                db.session.commit()
                return jsonify('success')
            if type == 'timeend':
                record = Userrecord.query.filter(Userrecord.ureID == request.form.get('id')).first()
                record.timeend = request.form.get('timeend')
                record.urestatus = '已完成约看'
                db.session.commit()
                return jsonify('success')
        if menu == 'rent1':
            # 解除租约
            house = House.query.filter(House.houseID == request.form.get('hid')).first()
            house.housestatus = 1
            db.session.commit()
            record = Rentrecord.query.filter(Rentrecord.reID == int(request.form.get('reid'))).first()
            record.checkout = date.today()
            record.status = '已结束'
            db.session.commit()
            return jsonify('success')
        if menu == 'rent2':
            type = request.form.get('type')
            if type == 'checkhouseid':
                houseid = request.form.get('houseid')
                house = House.query.filter(House.houseID == houseid, House.housestatus == 1).first()
                if house:
                    return jsonify('ok')
                else:
                    return jsonify('nodata')
            if type == "checktel":
                tel = request.form.get('tel')
                user = User.query.filter(User.usertel == tel).first()
                if user:
                    return jsonify('success')
                else:
                    return jsonify('nodata')
            if type == "rent":
                house = House.query.filter(House.houseID == request.form.get('houseid')).first()
                house.housestatus = 0
                house.tenanttel = request.form.get('tenanttel')
                db.session.commit()
                payment = request.form.get('payment').replace(u'付',"")
                record = Rentrecord (retime = date.today(),repayment = payment,rerent = int(request.form.get('rent')),
                                     redeposit = int(request.form.get('deposit')),reservice = int(request.form.get('service')),
                                     checkin = request.form.get('checkin'),checkout = request.form.get('checkout'),
                                     usertel = request.form.get('tenanttel'),houseID = request.form.get('houseid'), status='进行中')
                db.session.add(record)
                db.session.commit()
                return jsonify('success')
        if menu == 'info':
            type = request.form.get('type')
            if type == 'save':
                name = request.form.get('name')
                manager = Manager.query.filter(Manager.mantel == session['mantel']).first()
                manager.manname = name
                session['manname'] = name
                db.session.commit()
                return jsonify(name)
            if type == 'psw':
                manager = Manager.query.filter(Manager.mantel == session['mantel']).first()
                manager.manpsw = request.form.get('psw')
                session['manpsw'] = request.form.get('psw')
                db.session.commit()
                return jsonify('success')
            if type == 'cancel':
                manager = Manager.query.filter(Manager.mantel == session['mantel']).first()
                session['manname'] = manager.manname
                return jsonify(manager.manname)
            return render_template('admin/adminInfo.html')

if __name__ == '__main__':
    app.run()
