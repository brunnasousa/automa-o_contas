"""
-> Feito por: Brunna Sousa <-
Aqui é fornecido uma lista de email atraves do arquivo conta.xlsx
e faz o comparativo com base.xlsx

RESULTADO:
1 - Ele verifica e tras no console a quantidade de 'ATIVOS', 'DESATIVADOS', e também diz se não encontrou, assim como as porcentagem e total
2 - Diz o status dos emails, e por fim apenas a coluna do status.
"""


import pandas as pd

# Caminhos dos arquivos
base_data_path = 'limoeiro teste.xlsx'
emails_to_check_path = 'teste2.xlsx'



# Definição da função para verificar o status dos e-mails
def check_status(email, df_base):
    match = df_base[df_base['Email Address [Required]'] == email]['Last Sign In [READ ONLY]']
    if not match.empty:
        return 'DESATIVADO' if match.iloc[0] == 'Never logged in' else 'ATIVADA'
    else:
        return 'EMAIL NÃO ENCONTRADO'

# Carregando os dados das planilhas
df_base = pd.read_excel(base_data_path)
df_emails_to_check = pd.read_excel(emails_to_check_path)

# Selecionando a primeira coluna de 'conta.xlsx', que corresponde à coluna 'A'
email_column = df_emails_to_check.columns[0]  # Isso pega o nome da primeira coluna

# Aplicando a função para verificar o status dos e-mails em 'conta.xlsx'
df_emails_to_check['Status'] = df_emails_to_check[email_column].apply(lambda email: check_status(email, df_base))

# Calculando as estatísticas baseado nos status dos e-mails verificados
status_counts = df_emails_to_check['Status'].value_counts()
total_emails = df_emails_to_check.shape[0]
status_percentage = (status_counts / total_emails) * 100

# Adicionando a contagem total
status_counts['TOTAL'] = total_emails

# Exibindo os resultados no console
print("------------------------------")
print("Quantitativo e Porcentagem de Status baseado em 'conta.xlsx':")
print(status_counts)
print(status_percentage)

# Suponha que 'df_emails_to_check' já está definido e inclui as colunas de interesse
email_column = 'Email'  # Substitua 'Email' pelo nome real da sua coluna de e-mail, se diferente

# Exibindo o status de cada e-mail
print("\nStatus dos e-mails da planilha 'conta':")
print(df_emails_to_check[[email_column, 'Status']])

# Salvando os dados em uma planilha Excel
with pd.ExcelWriter('Status_Emails.xlsx', engine='openpyxl') as writer:
    df_emails_to_check[[email_column, 'Status']].to_excel(writer, index=False)