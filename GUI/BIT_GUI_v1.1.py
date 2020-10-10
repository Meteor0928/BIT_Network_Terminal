# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsgbox
import re, os, base64
import requests

class User_Info():
    def __init__(self):
        self.userPath = os.getcwd()
        self.userFile = os.path.join(self.userPath, 'BIT_info')

    def getUserInfo(self):
        try:
            with open(self.userFile, 'rt') as f:
                us_info = f.readlines()
                u_name = us_info[0][: -1]
                u_pwd = us_info[1][: -1]
            u_pwd = base64.decodebytes(bytes(u_pwd, 'utf-8')).decode()
        except:
            u_name = ''
            u_pwd = ''
        return u_name, u_pwd
    
    def saveUserInfo(self, userInfo):
        if not os.path.exists(self.userFile):
            u_pwd = base64.encodebytes(bytes(userInfo[1], 'utf-8')).decode()
            with open(self.userFile, 'wt') as f:
                f.write(userInfo[0]+'\n')
                f.write(u_pwd+'\n')
        else:
            pass


class BIT_Network():
    def __init__(self, userInfo):
        self.web_port = 801        
        self.url_init = 'http://10.0.0.55:{}'.format(self.web_port)
        
        self.u_name = userInfo[0]
        self.u_pwd = userInfo[1]
        
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': '10.0.0.55:{}'.format(self.web_port),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        self.url_BIT = self.url_init + '/include/auth_action.php'
        self.url_info = self.url_init + '/srun_portal_pc_succeed.php'
        self.url_logout = self.url_init[:-4] + '/cgi-bin/srun_portal'
        
        self.bit = requests.session()
        
    def login(self):
        self.data_login = {
            'username': self.u_name,
            'password': self.u_pwd,
            'ac_id': '1',
            'save_me': '0',
            'ajax': '1',
            'action': 'login',
        }
        
        self.bit_login = self.bit.post(self.url_BIT, data=self.data_login, headers=self.headers)
        self.bit_login.encoding = 'utf-8'
        self.bit_html = self.bit_login.text.lower()

        if 'login_ok' in self.bit_html:
            output_init = 'Welcome to connect BIT network!'
            self.response_test = self.bit.get(self.url_info, headers=self.headers)
            re_P = r'<span.*?>(.*?)</span>'
            self.user_info = re.findall(re_P, self.response_test.text)
            self.us_name = self.user_info[0].strip()
            self.us_ip = self.user_info[1].strip()
            self.us_bytes = self.user_info[2].strip()
            self.us_balance = self.user_info[4].strip()
            output = '{0}\n\nUsername: {1}\nLogin IP: {2}\nUsed Bytes: {3}\nBalance: {4}'.format(output_init, self.us_name, self.us_ip, self.us_bytes, self.us_balance)
            return output
        elif 'ip has been online' in self.bit_html:
            output_init = 'IP has been Online!'
            self.response_test = self.bit.get(self.url_info, headers=self.headers)
            re_P = r'<span.*?>(.*?)</span>'
            self.user_info = re.findall(re_P, self.response_test.text)
            self.us_name = self.user_info[0].strip()
            self.us_ip = self.user_info[1].strip()
            self.us_bytes = self.user_info[2].strip()
            self.us_balance = self.user_info[4].strip()
            output = '{0}\n\nUsername: {1}\nLogin IP: {2}\nUsed Bytes: {3}\nBalance: {4}'.format(output_init, self.us_name, self.us_ip, self.us_bytes, self.us_balance)
            return output
        elif 'password is error' in self.bit_html:
            output = 'Password is Error!'
            return output
        elif 'arrearage' in self.bit_html:
            output = 'Arrearage User!'
            return output
        else:
            output = 'Error occurs during connecting network ...'
            return output
    
    def logout(self, type='y'):
        self.data_logout = {
            'username': self.u_name,
            'password': None,
            'ac_id': '1',
            'type': '2',
            'action': 'logout',
        }
        if type == 'n':
            self.data_logout['password'] = self.u_pwd
        
        self.bit_logout = self.bit.post(self.url_logout, data=self.data_logout, headers=self.headers)
        self.bit_logout.encoding = 'utf-8'

        self.bit_html = self.bit_logout.text.lower().strip()
        if 'logout_ok' in self.bit_html:
                output = 'IP has been logouted!'
        else:
            output = 'Note:\n\nIP has been logouted, or Some Error occur during logouting IP'
        return output
            

class BIT_Windows():
    def __init__(self, master):
        self.root = master
        self.root.title('BIT Network System')
        self.root.geometry('420x350')
        self.root.resizable(0, 0)
        if os.path.exists(r'.\BIT_GUI.ico'):
            self.root.iconbitmap(r'.\BIT_GUI.ico')
        
        self.UserInfo = User_Info()
        self.us_info = self.UserInfo.getUserInfo()
        
        
        self.mainFrame_top = ttk.Frame(self.root)
        self.mainFrame_top.grid(row=0, column=0, padx=27.5, pady=10)
        
        self.mainLabel = tk.Label(self.mainFrame_top, text='Welcome to the BIT Network Authentication System', font=('Times', 12, 'bold'), anchor='center', background='pink')
        self.mainLabel.grid(row=0, column=0, columnspan=3, pady=10, ipadx=4)

        self.user = tk.Label(self.mainFrame_top, width=12, text='Username: ', bg='orange', fg='#00B') 
        self.user.grid(row=1, column=0, pady=5, sticky='e')
        self.pwd = tk.Label(self.mainFrame_top, width=12, text='Password: ', bg='orange', fg='#00B')
        self.pwd.grid(row=2, column=0, pady=5, sticky='e')

        self.var_username = tk.StringVar()
        self.var_username.set(self.us_info[0])
        self.var_pwd = tk.StringVar()
        self.var_pwd.set(self.us_info[1])
        self.userEntry = tk.Entry(self.mainFrame_top, textvariable=self.var_username, width=15)
        self.userEntry.grid(row=1, column=1, pady=5)
        self.userEntry.focus_set()
        self.pwdEntry = tk.Entry(self.mainFrame_top, textvariable=self.var_pwd, width=15, show='*')
        self.pwdEntry.grid(row=2, column=1, pady=5)
        
        self.var_radio = tk.StringVar()
        self.var_radio.set('y')
        self.radio_1 = tk.Radiobutton(self.mainFrame_top, text='Local Network', width=12, variable=self.var_radio, anchor='w', value='y')
        self.radio_1.grid(row=1, column=2, pady=5, sticky='w')
        self.radio_2 = tk.Radiobutton(self.mainFrame_top, text='All Networks', width=12, variable=self.var_radio, anchor='w', value='n')
        self.radio_2.grid(row=2, column=2, pady=5, sticky='w')
        
  
        self.mainFrame_middle = ttk.Frame(self.root)
        self.mainFrame_middle.grid(row=1, column=0, pady=10)
        
        self.login = tk.Button(self.mainFrame_middle, text='Login', width=8, bg='lightskyblue', fg='red', command=self.usr_login)
        self.login.grid(row=0, column=0, padx=15)
        self.clear = tk.Button(self.mainFrame_middle, text='Clear', width=8, bg='silver', fg='red', command=self.clear_info)
        self.clear.grid(row=0, column=1, padx=15)
        self.logout = tk.Button(self.mainFrame_middle, text='Logout', width=8, bg='lightgreen', fg='red', command=self.usr_logout)
        self.logout.grid(row=0, column=2, padx=15)
        

        self.mainFrame_down = ttk.Frame(self.root)
        self.mainFrame_down.grid(row=2, column=0, pady=15)
        
        self.Output = tk.Text(self.mainFrame_down, width=30, height=6, bg='lightblue', font=('Microsoft YaHei', 10, 'normal'), padx=5, pady=5)
        self.Output.pack(expand=1, fill='both')
        self.Output.bind("<Key>", lambda _: "break")
    
    def usr_login(self):
        self.usr_name = self.var_username.get().strip()
        self.usr_pwd = self.var_pwd.get().strip()
        self.userinfo = [self.usr_name, self.usr_pwd]
        if len(self.usr_name) != 0 and len(self.usr_pwd) != 0:
            BIT = BIT_Network(self.userinfo)
            msg_info = BIT.login()
            if self.usr_name in msg_info:
                self.UserInfo.saveUserInfo(self.userinfo)
        else:
            msg_info = 'Your user information is not complete!'
        self.show_msg(msg_info)

    def show_msg(self, Msg_info):
        self.Output.delete(0.0, tk.END)
        self.Output.insert(tk.END, Msg_info)
    
    def clear_info(self):
        self.var_username.set('')
        self.var_pwd.set('')
        self.var_radio.set('y')
        self.Output.delete(0.0, tk.END)

    def usr_logout(self):
        self.usr_name = self.var_username.get().strip()
        self.usr_pwd = self.var_pwd.get().strip()
        self.usr_radio = self.var_radio.get().strip()
        self.userinfo = [self.usr_name, self.usr_pwd]
        if len(self.usr_name) != 0 and len(self.usr_pwd) != 0:
            BIT = BIT_Network(self.userinfo)
            msg_info = BIT.logout(type=self.usr_radio)
        else:
            msg_info = 'Your user information is not complete!'
        self.show_msg(msg_info)
        
def main():
    root = tk.Tk()
    BIT = BIT_Windows(root)
    root.mainloop()

    
if __name__ == '__main__':
    main()
