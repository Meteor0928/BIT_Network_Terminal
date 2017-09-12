# -*- coding: utf-8 -*-

import os, random
import platform
import getpass
import requests
from bs4 import BeautifulSoup as BS

web_port = random.randrange(801, 805, 1)

def getFilePath(us_name):
    if platform.system() == 'Windows':
        File_Path = 'C:\\Users\\' + us_name + '\\AppData\Local\\BIT_Network'
        return File_Path

users = getpass.getuser()
user_path = getFilePath(users)
user_file = user_path + '\\BIT_info'

if os.path.exists(user_path) == False:
    os.mkdir(user_path)

if os.path.exists(user_file):
    with open(user_file, 'rt') as fd:
        user_info = fd.readlines()
        u_name = user_info[0][: -1]
        u_pwd = user_info[1][: -1]
else:
    u_name = input('Please input your username: ')
    u_pwd = input('Please input your password: ')
    with open(user_file, 'wt') as fd:
        fd.write(u_name+'\n')
        fd.write(u_pwd+'\n')

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": url_web[7: ],
    "Origin": url_web,
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

url_init = 'http://10.0.0.55'
url_web = url_init + ':' + str(web_port)

url_login = url_web + '/include/auth_action.php'
url_logout = url_web + '/srun_portal_pc_succeed.php'

data = {
    'username': u_name,
    'password': u_pwd,
    'ac_id': '1',
    'save_me': '0',
    'ajax': '1',
    'action': 'login',
}

s_BIT = requests.session()
response_login = s_BIT.post(url_login, data=data, headers=headers)

html = response_login.text.lower()

if 'login_ok' in html:
    print('Welcom to connect BIT network!\n')
    print('>--**************************--<')
    response_test = s_BIT.get(url_logout, headers=headers)
    soup_BIT = BS(response_test.text, 'lxml')       ## 'lxml' to 'html5lib'
    user_info = soup_BIT.find_all('tr', {'height':'30'})
    us_name = user_info[0].span.string.strip()
    us_ip = user_info[1].span.string.strip()
    us_bytes = user_info[2].span.string.strip()
    us_balance = user_info[4].span.string.strip()
    print('username: {0}'.format(us_name))
    print('Login IP: {0}'.format(us_ip))
    print('Used Bytes: {0}'.format(us_bytes))
    print('Balance: {0}'.format(us_balance))
elif 'IP has been online' in response_login.text:
    print('IP has been Online, Please logout!')
elif 'Password is error' in response_login.text:
    print('Password is Error!')
else:
    print('Error occurs during connecting network...')
print('>--**************************--<')
input('\nTurn off the terminal by pressing <Enter> key...')
