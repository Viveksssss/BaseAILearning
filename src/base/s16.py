import re
from urllib import request, parse
from urllib import error

page = 1
url = "https://www.qiushibaike.com/hot/page/" + str(page)
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
files = open("findfile.txt", "w+", encoding="utf-8")
try:
    req = request.Request(url)
    req.add_header("User-Agent", user_agent)
    response = request.urlopen(req)
    # bytes变为字符串
    content = response.read().decode("utf-8")
    pattern = re.compile(
        r'<div.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?number">(.*?)</i>.*?'
        + r'"number">(.*?)</i>',
        re.S,
    )
    result = re.findall(pattern, content)
    
    for item in result:
        author = item[0]
        contant = item[1]
        vote = "赞：" + item[2]
        commit = "评论数：" + item[3]
        infos = vote + " " + commit + " " + "\n\n"
        print(author)
        print(contant)
        print(infos)
        files.write(author)
        files.write(contant)
        files.write(infos)


except error.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)
finally:
    files.close()
