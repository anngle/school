# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash,current_app,render_template,request
import time,random,hashlib
from functools import wraps



import datetime 

#生成无重复随机数
gen_rnd_filename = lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))
#文件名合法性验证
allowed_img_lambda = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in set(['jpg', 'png'])



def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def create_file_name(f):
    choice_str = 'ABCDEFGHJKLNMPQRSTUVWSXYZ'
    str_time =  time.time()
    username_str = str(int(str_time))
    for i in range(6):
        username_str += random.choice(choice_str)
    filename = hashlib.md5(username_str.encode('utf-8')).hexdigest()[:32]+'.'+f.filename.rsplit('.', 1)[1]
    return filename

def allowed_file(filename):
    if '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS_FILES'] :
        return True
    else:
        return False
