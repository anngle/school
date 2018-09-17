import re



def allow_ask_leave(data=''):
    print(f'allow_ask_leave:{data}')

def no_allow_ask_leave(data=''):
    print(f'no_allow_ask_leave:{data}')
commands = {
    '^同意请假\w': ['同意请假',allow_ask_leave],
    '^不同意请假\w': ['不同意请假',no_allow_ask_leave],
}
re_str = '同意请假1djakdjlakj00'
ma_str = '^请假\d'


for k in commands:
    if re.match(k, re_str):
        print(commands[k][0])
        re_str = re_str.replace(commands[k][0],'').strip()
        commands[k][1](re_str)


if re.match(ma_str, re_str):
    print(re_str)
    re_str = re_str.replace('请假','').strip()
    print(re_str)
else:
    print(0)