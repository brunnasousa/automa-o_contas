import pandas as pd
import unicodedata

# Exemplo de dados
data = {
        'Nome Completo': ['Brunna Danielle Santos de Sousa', 'Brunna Danielle Castro dos Sousa', 'Arroz Com Feijão', 'Brunna Danielle Paiva dos Sousa', 'Brunna Paiva Costa dos Sousa']
}
df = pd.DataFrame(data)

# Função para remover caracteres especiais e acentos
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

# Função para gerar e-mail a partir do nome, excluindo preposições
def gerar_email(partes, emails_gerados, dominio='dominio.exemplo.com'):
    # Definir uma lista de palavras para excluir do e-mail
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    
    # Filtrar as partes excluídas e não alfabéticas
    partes_email = [parte for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    
    # Tentativa inicial: usar o primeiro e o último nome (após filtrar)
    email = f"{partes_email[0].lower()}.{partes_email[-1].lower()}@{dominio}"
    if email not in emails_gerados:
        return email
    
    # Se o e-mail já existir, tente usar outro nome do meio
    for parte in partes_email[1:-1]:
        email = f"{partes_email[0].lower()}.{parte.lower()}@{dominio}"
        if email not in emails_gerados:
            return email
    
    # Se todas as tentativas falharem, adicione um número ao e-mail
    sufixo = 1
    email_base = f"{partes_email[0].lower()}.{partes_email[-1].lower()}"
    while f"{email_base}{sufixo}@{dominio}" in emails_gerados:
        sufixo += 1
    return f"{email_base}{sufixo}@{dominio}"

# Função para processar o nome e criar o e-mail
def processar_nome(nome, emails_gerados):
    nome = remover_acentos(nome)  # Remover acentos
    partes = nome.split()
    primeiro_nome = partes[0].capitalize()
    nome_formatado = ' '.join([p.capitalize() for p in partes])
    resto_nome = ' '.join([p.capitalize() for p in partes[1:]])  # Incluir todas as palavras
    
    email = gerar_email(partes, emails_gerados)
    emails_gerados.add(email)

    return pd.Series([nome_formatado, primeiro_nome, resto_nome, email])

# Conjunto para armazenar e-mails gerados
emails_gerados = set()

# Aplicar a função de processamento e dividir em novas colunas
df[['Nome Formatado', 'Primeiro Nome', 'Resto Nome', 'E-mail']] = df.apply(lambda row: processar_nome(row['Nome Completo'], emails_gerados), axis=1)

# Exibir o resultado
print(df[['Nome Formatado', 'Primeiro Nome', 'Resto Nome', 'E-mail']])
