import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#configurando a organização do devops
organizacao = 'organização'
projeto = 'projeto'
pat = 'pat' #token
iteracao = 'iteração\Sprint 1'

#informações do email 
from_address = "email@email.com"
to_addresses = ["emaildestinatario@email.com", "emaildestinatario@email.com"]
assunto = "Teste"
corpo_email = ""

#autenticação e conexão
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {pat}'
}

#consultando work item
wiql_query = f"""
SELECT [System.Id], [System.Title], [System.Description]
FROM WorkItems
WHERE [System.IterationPath] = '{iteracao}'
"""

url = f"https://dev.azure.com/{organizacao}/{projeto}/_apis/wit/wiql?api-version=6.0"
response = requests.post(url, headers=headers, json={"query": wiql_query})

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
  work_items = response.json().get('workItems', [])

  #buscando detalhes dos cards
  for item in work_items:
    work_item_id = item['id']
    work_item_url = f"https://dev.azure.com/{organizacao}/{projeto}/_apis/wit/workitems/{work_item_id}?api-version=6.0"
    work_item_response = requests.get(work_item_url, headers=headers)
    work_item_data = work_item_response.json()

    description = work_item_data['fields'].get('System.Description', None)
    if not description:
      corpo_email += f"Adicione o tuite de PO a tempo do comite de projetos\n"
else:
  # Lidar com o erro
  print(f"Requisição falhou com o código de status {response.status_code}")
  print(response.text)

#criando a mensagem se o campo descrição for vazio
if corpo_email != "":
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(from_address, "senha de app")

  msg = MIMEMultipart()
  msg['From'] = from_address
  msg['To'] = ", ".join(to_addresses)
  msg['Subject'] = assunto

  msg.attach(MIMEText(corpo_email, 'plain'))

  #enviando o email
  server.sendmail(from_address, to_addresses, msg.as_string())

  #fechando o servidor
  server.quit()