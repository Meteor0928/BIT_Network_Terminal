import httplib
import urllib
import time

host = '10.0.0.55'
port = 801


def post_data(host, port, url, params):
    http_client = None
    params = urllib.urlencode(params)
    try:
        http_client = httplib.HTTPConnection(host, port)
        http_client.request('POST', url, params, headers={"Content-type": "application/x-www-form-urlencoded",
                                                          "Accept": "text/plain"})
        response = http_client.getresponse()
        return response.status, response.read()
    except Exception, e:
        print e
    finally:
        if http_client:
            http_client.close()


def get_data(host, port, url, params):
    http_client = None
    params = urllib.urlencode(params)
    print params
    try:
        http_client = httplib.HTTPConnection(host, port)
        http_client.request('GET', url, params, headers={"Content-type": "application/x-www-form-urlencoded",
                                                          "Accept": "text/plain"})
        response = http_client.getresponse()
        return response.status, response.read()
    except Exception, e:
        print e
    finally:
        if http_client:
            http_client.close()


def login(username, password):
    status, content = post_data(host, port, '/include/auth_action.php',
                                {'action': 'login',
                                 'username': username, 'password': password,
                                 'ac_id': '1', 'user_ip': '', 'nas_ip': '', 'user_mac': '', 'save_me': '1',
                                 'ajax': '1'})
    print status, content
    if status == 200 and content.startswith('login_ok'):
        return True
    else:
        return False


def logout(username, password):
    status, content = post_data(host, port, '/include/auth_action.php',
                                {'action': 'logout',
                                 'username': username, 'password': password,
                                 'ajax': '1'})


def main():
    username = ''   # 用户名
    password = ''   # 密码
    
    while True:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        login(username, password)
        time.sleep(600)

if __name__ == '__main__':
    main()
