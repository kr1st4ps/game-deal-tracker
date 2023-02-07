from email.message import EmailMessage
import ssl
import smtplib
#TODO add config

def send(message, console):
    sender = "kristaps.almanis14@gmail.com"
    password = "leazlkawfhwezyzf"

    receiver = "kristaps.almanis14@gmail.com"

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