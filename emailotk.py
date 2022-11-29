import smtplib
import ssl
from email.message import EmailMessage
import otk


class emailauto:
    def __init__(self):
        self.subject = "Sitti OTK"
        self.senderEmail = "pythoncfugs@gmail.com"
        self.emailpass = "Cfugstest"
        self.onetime = otk.emailKey()
    
    def sendOTK(self, email):
        self.userMail = email
        # self.keySend = self.onetime.getKey()
        self.message = EmailMessage()
        self.message["From"] = self.senderEmail
        self.message["To"] = email
        self.message["Subject"] = self.subject
        # self.message.set_content(self.keySend)

        # self.context = ssl.create_default_context()
        # with smtplib.SMTP_SSL("smtp.gmail.com", 456, context=self.context) as server:
        #     server.login(self.senderEmail, self.emailpass)
        #     server.sendmail(self.senderEmail, self.userMail, self.message.as_string)








