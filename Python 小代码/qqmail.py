import smtplib as sl #导入内置模块smtplib，通过该模块的类SMTP_SSL，创建了一个实例对象qqMail
from email.mime.multipart import MIMEMultipart # email模块的类MIMEMultipart，可以整合邮件头、正文和附件等信息
from email.header import Header #email模块的类Header，用于设置邮件头，即邮件的主题，收发件人
from email.mime.text import MIMEText #构建邮件正文，需要从email.mime.text中导入MIMEText类示例中，为导入MIMEText类的固定写法
from email.mime.image import MIMEImage #设置图片附件，需要从email.mime.image中导入MIMEImage类

#收发件人和基本设置
qqMail = sl.SMTP_SSL("smtp.qq.com", 465)
mailName = "xiangtian_030611@qq.com"
mailPassword = "svqketybpfmnbigg" #QQ邮箱授权码
qqMail.login(mailName , mailPassword)
sender = "xiangtian_030611@qq.com" #发件人
receiver = "136733984@qq.com" #收件人
#正文
message = MIMEMultipart()
message["Subject"] = Header("Python")
message["From"] = Header(f"Python<{sender}>")
message["To"] = Header(f"Xiangtian<{receiver}>")
textWord = "这是一个Python程序"
mailStyle = MIMEText(textWord,"plain","utf-8") #第一个参数是文本内容，即我们需要发送邮件的正文内容;
                                                                 #第二个参数是文本格式，表示我们的正文内容以何种格式展示;
                                                                 #第三个参数是编码。"utf-8"编码，能防止中文乱码
#图片附件
filePath = r"/home/xt/桌面/cheshire.jpg"
with open(filePath, "rb") as imageFile: #第一个参数是路径(路径前面加r来防止转义);第二个参数是打开方式，用特定的字符串表示
    fileContent = imageFile.read()
attachment = MIMEImage(fileContent)
attachment.add_header("Content-Disposition", "attachment", filename="cheshire.jpg") #设置附件标题
#将正文和附件加入到邮件中
message.attach(mailStyle)
message.attach(attachment)
#发送
qqMail.sendmail(sender, receiver, message.as_string())
