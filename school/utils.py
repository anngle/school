# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash,current_app
import time,random,hashlib

def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)




def create_file_name(f):
    choice_str = 'ABCDEFGHJKLNMPQRSTUVWSXYZ'
    str_time =  time.time()
    username_str = str(int(str_time))
    for i in range(6):
        username_str += random.choice(choice_str)
    filename = hashlib.md5(username_str).hexdigest()[:32]+'.'+f.filename.rsplit('.', 1)[1]
    return filename

def allowed_file(filename):
    if '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS_FILES'] :
        return True
    else:
        return False
