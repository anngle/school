# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

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
    



@blueprint.route('/introduction')
@templated()
def introduction():
    return dict()
    


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







