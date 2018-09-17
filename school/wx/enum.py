#codingutf-8

from .enum_func import *

# 指令列表
commands = {
    '^同意请假\d': ['同意请假',allow_ask_leave], 
    '^不同意请假\d': ['不同意请假',reject_allow_ask_leave],  
    '^修改账号\w': ['修改账号',change_username],  
    '^修改密码\w': ['修改密码',change_password],   
    '^同意该教师\d': ['同意该教师',allow_reg_teacher], 
}
