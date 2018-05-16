# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for,current_app,send_from_directory
from flask_login import login_required, login_user, logout_user
import qrcode

import pyqrcode
from io import StringIO,BytesIO

from flask import make_response
import image,os
# try:
#     from PIL import Image
# except Exception as e:
#     print(str(e))
#     print('=====')
#     # import Image
#     from PIL.Image import core as image


from school.extensions import login_manager
from school.public.forms import LoginForm
from school.user.forms import RegisterForm
from school.user.models import User
from school.utils import flash_errors,templated

blueprint = Blueprint('public', __name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Home page."""
    return render_template('public/home.html')


@blueprint.route('/user_info')
@templated()
def user_info():
    return dict()
    

#简介
@blueprint.route('/introduction')
@templated()
def introduction():
    return dict()


#获取学生二维码
@blueprint.route('/get_student_rq/<int:student_str>')
def get_student_rq(student_str='0'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(f'S{student_str}')
    qr.make(fit=True)
    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    response = make_response(img_io.read())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Description'] = 'attachment; filename=%i.png' % student_str
    return response

#获取学生头像
@blueprint.route('/get_student_img')
@blueprint.route('/get_student_img/<path:student_img>')
def get_student_img(student_img='0'):
    path = os.getcwd()+'/'+current_app.config['STUDENTS_IMG']
    return send_from_directory(path, student_img)

    
    
    


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


#flask-sse test
@blueprint.route('/hello')
def publish_hello():
    sse.publish({"user": "alice", "status": "Life is good!"}, type='greeting')
    # sse.publish({"message": "anaf!"}, type='greeting')
    return "Message sent!"
"""
<script>
    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('greeting', function(event) {
        var data = JSON.parse(event.data);
        document.getElementById('inohtml').innerHTML +='<br/>hello';
        // alert(data);
    }, false);
    source.addEventListener('error', function(event) {
        // alert("Failed to connect to event stream. Is Redis running?");
    }, false);
  </script>
"""







