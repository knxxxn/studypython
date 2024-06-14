import smtplib
from email.mime.text import MIMEText

send_email_1 = "네이버아이디@naver.com"
send_email_2 = "구글아이디@gmail.com"
send_pwd_1 = "네이버비밀번호"
send_pwd_2 = "구글비밀번호"

recv_email = "받는이메일 주소@gmail.com"

smtp_name_1 = "smtp.naver.com"
smtp_name_2 = "smtp.gmail.com"
smtp_port = 587

text = """
메일 내용 와라라라랄
길게 써도 가능
"""

msg = MIMEText(text)

msg['Subject'] = "시험용 프로젝트"
msg['From'] = send_email_1, send_email_2
msg['To'] = recv_email
print(msg.as_string())

n=smtplib.SMTP(smtp_name_1, smtp_port)
n.starttls()
n.login(send_email_1, send_pwd_1)
n.sendmail(send_email_1, recv_email, msg.as_string())
n.quit()

g=smtplib.SMTP(smtp_name_2, smtp_port)
g.starttls()
g.login(send_email_2, send_pwd_2)
g.sendmail(send_email_2, recv_email, msg.as_string())
g.quit()