# -*- coding: utf-8 -*-

import os, re, getpass, base64
import requests

web_port = 801

user_file = os.path.join(os.getcwd(),'BIT_info')            # The file including username and password 

try:
    with open(user_file, 'rt') as fd:
        user_info = fd.readlines()
        u_name = user_info[0][: -1]
        u_pwd = user_info[1][: -1]
    u_pwd = base64.decodebytes(bytes(u_pwd, 'utf-8')).decode()
except FileNotFoundError:
    u_name = input('Please input your username: ')
    u_pwd = getpass.getpass('Please input your password: ')
    u_pwd = base64.encodebytes(bytes(u_pwd, 'utf-8')).decode()
    with open(user_file, 'wt') as fd:
        fd.write(u_name+'\n')
        fd.write(u_pwd+'\n')


url_init = 'http://10.0.0.55'
url_web = '{}:{}'.format(url_init,str(web_port))
url_login = '{}/include/auth_action.php'.format(url_web)
url_logout = '{}/srun_portal_pc_succeed.php'.format(url_web)

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    'Cache-Control': 'no-cache',
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": '10.0.0.55:{}'.format(web_port),
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

data = {
    'username': u_name,
    'password': u_pwd,
    'ac_id': '1',
    'save_me': '0',
    'ajax': '1',
    'action': 'login',
}

while True:
    s_BIT = requests.session()
    response_login = s_BIT.post(url_login, data=data, headers=headers)
    html_init = response_login.text
    html = html_init.lower()
    if 'login_ok' in html:
        break
    if 'IP has been online' in html_init:
        break
