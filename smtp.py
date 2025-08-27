import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Paramètres
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PWD")
outlook_smtp = 'smtp.office365.com'
port = 587
recipient_email = os.getenv("RECIPIENT_EMAIL")
subject = 'Test HTML Email'
html_content = """
<html>
  <body>
    <h1 style="color:blue;">Bonjour !</h1>
    <p>Ceci est un email HTML envoyé depuis Python.</p>
  </body>
</html>
"""

# Création du message
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(html_content, 'html'))

# Envoi via SMTP
try:
    server = smtplib.SMTP(outlook_smtp, port)
    print(f"server: {server}")
    res=server.starttls()  # sécurise la connexion
    print(f"server: {res}")
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email envoyé avec succès !")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    server.quit()
