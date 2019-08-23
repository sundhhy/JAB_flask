from flask import render_template, session, request, make_response, send_from_directory, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import album

from ..models import User, Photo
from .. import db
from config import static_path

PHOTO_IN_PAGE = 10


def request_get_parameter(key):
    return request.values.get(key)


def get_photo_by_user(name, page):
    u = User.query.filter_by(username=name).first()
    rlt = []
    if u is None:
        return rlt
    start_num = (page - 1) * PHOTO_IN_PAGE
    phs = Photo.query.filter_by(user=u).all()
    # phs = Photo.query.all()
    count = 0
    for i in range(len(phs)):
        if i >= start_num:
            ph = phs[i]
            a_rlt = {'title': ph.title, 'filename': ph.fileName}
            rlt.append(a_rlt)
            count += 1
        if count >= PHOTO_IN_PAGE:
            break

    return rlt


@album.route('/')
@login_required
def album_page():
    return render_template('album/album.html')


@album.route('/pageLoad')
@login_required
def page_load():
    res = ""
    try:
        cur_img = session['curImg']
        res = "$('#show').attr('src', \"{}\")\n".format(cur_img)
    except KeyError:
        pass
    res += "onLoadHandler()"
    return make_response(res), 200


@album.route('/getPhoto')
@login_required
def get_photo():
    name = current_user.username
    try:
        page_obj = session['curPage']
    except Exception:
        page_obj = None
    cur_page = 1 if page_obj is None else int(page_obj)

    try:
        photos = get_photo_by_user(name, cur_page)
        if len(photos) == 0:
            return make_response(''), 200
        res = "var list = $('#list').empty();"
        for ph in photos:
            res += '\n'
            res += "$(\"#list\").append(\"<div align='center'>" \
                   "<a href='javascript:void(0)' onclick=\\\"showImg('{}')\\\">" \
                   "{} </a></div>\")".format(ph['filename'], ph['title'])
            # res += "$(\"#list\").append(\"<div>{}</div>\")".format(ph['title'])
        return make_response(res), 200
    except Exception as e:
        return make_response("{}, 请重试".format(e)), 200


@album.route('/showImg')
def show_img():
    file_name = request.args.get('img')
    user_name = current_user.username
    file_path = url_for('static', filename="album/{}/{}".format(user_name, file_name))
    session['curImg'] = file_path
    res = make_response("$('#show').attr('src', \"{}\")".format(file_path))
    return res


@album.route('/proUpload', methods=['POST'])
def upload_file():
    user = User.query.filter_by(username=current_user.username).first()
    title = request_get_parameter('title')
    file = request.files.get('file')
    user_dir = os.path.join(current_app.static_folder, 'album\{}'.format(current_user.username))
    # 先创建对应用户的文件夹
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    # file_name = os.path.join(user_dir, '{}'.format(file.filename))
    file_name = os.path.join(user_dir, secure_filename(file.filename))
    file.save(file_name)

    photo = Photo(title=title, fileName=secure_filename(file.filename), user=user)
    db.session.add(photo)
    db.session.commit()
    return make_response('文件上传成功'), 200


@album.route('/turnPage')
def turn_page():
    flag = request.args.get('turn')
    try:
        page_obj = session['curPage']
    except KeyError:
        page_obj = None

    cur_page = int(page_obj) if page_obj is not None else 1
    if cur_page == 1 and flag == '-1':
        session['curPage'] = '1'
        return make_response("alert('现在已经是第一页，无法向前翻页')"), 200
    else:
        cur_page += int(flag)
        phs = get_photo_by_user(current_user.username, cur_page)
        if len(phs) == 0:
            cur_page -= int(flag)
            return make_response("alert('往后翻页找不到任何相片记录"
                                 "系统自动返回上一页')"), 200
        else:
            session['curPage'] = str(cur_page)
            return make_response(""), 200

