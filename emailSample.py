import smtplib, ssl

port = 465  # For SSL
smtp_server = "mail.gandi.net"
sender_email = "devauto@podor.org"  # Enter your address
receiver_email = "minzixiaocn@gmail.com"  # Enter receiver address
password = 'DataX123.'
message = """From: From Zixiao <zixiao@podor.org>
To: To Zixiao <minzixiaocn@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)