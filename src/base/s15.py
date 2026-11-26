import email
from email.header import Header
from email.mime.base import MIMEBase
from email.utils import formataddr, parseaddr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


msg_from = "v125250@163.com"
passwd = "TCqmwD74jcjWQJeS"
msg_to = "v125250@163.com"


subject = "python邮件测试"
content = (
    "<html><body><h1>Hello</h1>"
    + '<p>send by <a href="http://www.python.org">Python</a>...</p>'
)
msg = MIMEMultipart()
msg["Subject"] = Header(subject, "utf-8").encode()
msg["From"] = _format_addr("大胖熊 <%s>" % msg_from)
msg["To"] = msg_to

text = MIMEText(content, "html", "utf-8")
msg.attach(text)

with open(r"C:\Users\v1252\Documents\高嘉豪-15031482956.pdf", "rb") as f:
    # 设置附件名字
    mime = MIMEBase("image", "jpg", filename="简历.pdf")
    # 加上头信息
    mime.add_header("Content-Disposition", "attachment", filename="简历.pdf")
    mime.add_header("Content-ID", "<0>")
    mime.add_header("X-Attachment-Id", "0")
    # 读取内容放入附件
    mime.set_payload(f.read())
    # 用Base64编码
    email.encoders.encode_base64(mime)
    # 添加到MIMEMultipart中
    msg.attach(mime)

try:
    # s = smtplib.SMTP_SSL("smtp.163.com",465)
    s = smtplib.SMTP("smtp.163.com", 25)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print("发送成功")
except smtplib.SMTPException as e:
    print("发送失败")
finally:
    s.quit()


# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.utils import parseaddr, formataddr
# from email.mime.base import MIMEBase
# from email.mime.image import MIMEImage


# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr((Header(name, "utf-8").encode(), addr))


# msg_from = "XXXXXXXXXXXX@163.com"
# passwd = "XXXXX"
# msg_to = "XXXXXXXXX@qq.com"
# receivers = ["XXXXXXXXXX@qq.com"]
# subject = "python邮件测试附件"
# content = (
#     '<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!'
# )

# # 附件邮件对象
# msg = MIMEMultipart()
# msg["From"] = _format_addr("恋恋风辰 <%s>" % msg_from)
# msg["To"] = msg_to
# msg["Subject"] = Header(subject, "utf-8").encode()
# # 添加正文
# text = MIMEText(content, "html", "utf-8")
# msg.attach(text)

# # 添加附件就是创建一个MIMEBase对象，然后attach到msg上。
# with open("./email.jpg", "rb") as f:
#     # 设置附件名字
#     mime = MIMEImage(f.read())
#     # 加上头信息
#     mime.add_header("Content-Disposition", "attachment", filename="test.jpg")
#     mime.add_header("Content-ID", "`<image1>`")

#     # 添加到MIMEMultipart中
#     msg.attach(mime)

# try:
#     s = smtplib.SMTP("smtp.163.com", 25)
#     s.login(msg_from, passwd)
#     s.sendmail(msg_from, receivers, msg.as_string())
#     print("发送成功")
# except smtplib.SMTPException as e:
#     print("发送失败")
# finally:
#     s.quit()
