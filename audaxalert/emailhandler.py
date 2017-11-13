import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_ADDRESS = "audaxalert@gmail.com"
BCC_ADDRESS = "audaxalert@josephtechnology.net"

def send_email(address, subject, messageText):
    fromAddress = SENDER_ADDRESS
    toAddress = address

    msg = MIMEMultipart()
    msg["From"] = fromAddress
    msg["To"] = toAddress
    msg["Subject"] = subject
    msg.attach(MIMEText(messageText, "html"))

    username = SENDER_ADDRESS
    password = 'Jame5TK1rk'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login(username, password)
    text = msg.as_string()
    server.sendmail(fromAddress, [toAddress] + [BCC_ADDRESS], text)
    server.quit()

if __name__ == "__main__":
    send_email("jules@joseph-net.co.uk", "Audax Alert Test", "<b>this is a test</b><br><br>Please ignore this email");    