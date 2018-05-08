import requests,json
import urllib.parse
def line_notify_text(message):
    LINE_ACCESS_TOKEN = "wEWbmKQbDdCLQCND65X3te3zi6agQr49ZvuZYKsv7jU"
    url = "https://notify-api.line.me/api/notify"
    msg = urllib.parse.urlencode({"message":message})
    LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded','Authorization':'Bearer '+LINE_ACCESS_TOKEN}
    session = requests.Session()
    a = session.post(url,headers=LINE_HEADERS,data=msg)
    print(a.text)
