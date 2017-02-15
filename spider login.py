import http.cookiejar
import urllib.request
import urllib

url_start=r'http://www.zhihu.com/topic/19556498/questions?page='
hc=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(hc))
opener.addheaders=[('User-Agent','Mozilla/5.0(x11;Linux x86_64;rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]

def login():
    username=''
    password=''
    cap_url='https://www.zhihu.com/captcha.gif?r=1466595391805&type=login'
    cap_content=urllib.request.urlopen(cap_url).read()
    cap_file=open('/root/Desktop/cap.gif','wb')
    cap_file.write(cap_content)
    cap_file.close()
    captcha = raw_input('capture:')
    url='https://www.zhihu.com/login/phone_num'
    data=urllib.urlencode({"phone_num":name,"password":password,"captcha":captcha})
    print(urllib.request.urlopen(url, data).read())

if __name__=="__main__":
    login()
