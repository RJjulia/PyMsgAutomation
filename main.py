import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#informações do email 
from_address = "email@email.com"
to_addresses = ["emaildestinatario1@email.com", "emaildestinatario2@email.com"]
assunto = "Teste"
corpo_email = "Este e-mail se trata de um teste"

#criando a mensagem
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = ", ".join(to_addresses)
msg['Subject'] = assunto

msg.attach(MIMEText(corpo_email, 'plain'))

#configurando o email
server = smtplib.SMTP("smtp.gmail.com", 587) #porta do provedor gmail
server.starttls()

server.login(from_address, "senha de app gerada no email")

#enviando o email
server.sendmail(from_address, to_addresses, msg.as_string())

#fechando o servidor
server.quit()