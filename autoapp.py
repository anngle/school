# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from school.app import create_app
from school.settings import DevConfig, ProdConfig
import logging

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

# 日志系统配置
handler = logging.FileHandler('loggings.log', encoding='UTF-8')
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)