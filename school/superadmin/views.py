# -*- coding: utf-8 -*-
"""Superadmin views."""
from flask import Blueprint, render_template


blueprint = Blueprint('superadmin', __name__, url_prefix='/superadmin', static_folder='../static/superadmin', template_folder='../templates/superadmin')



@blueprint.route('/')
def home():
    return render_template('home.html')






