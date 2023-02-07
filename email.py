from email.message import EmailMessage
import ssl
import smtplib
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

#TODO prettify code

def send(message, console):
    sender = config["USER_DEFINED"]["EMAIL_SENDER"]
    password = config["USER_DEFINED"]["EMAIL_PASSWORD"]

    receiver = config["USER_DEFINED"]["EMAIL_RECEIVER"]

    if console == "PS4":
        subject = "New PS4 game deals you might like..."

    body = message

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
        smpt.login(sender, password)
        smpt.sendmail(sender, receiver, em.as_string())