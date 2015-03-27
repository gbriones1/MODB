import smtplib, getpass
from database.models import Configuration

def send_email(destination, subject, text):
    success = False
    conf = Configuration.objects.all()[0]
    gmail_user = conf.sender_email
    gmail_pwd = conf.password
    FROM = conf.sender_email
    TO = [destination]
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), subject, text)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        #server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message.encode('ascii', 'ignore'))
        server.close()
        success = True
        print 'Successfully sent the mail'
    except Exception as e:
        print "Failed to send mail"
    return success

