'''
Criação de Email institucional:
1 - Fornecer a base de dados do Google = (df_base) base.xlsx 
2 - Forncecer a lista com os Nomes que ele deve verificar e fazer a criação = (df_teste) teste.xlsx 

---
Ele vai retornar um arquivo (df_resultado_final) = criacaoDeContas.xlsx 
com base no dominio fornecido dominio = dominio.exemplo.com

'''
import pandas as pd
import unicodedata

# Carregar a base de dados
df_base = pd.read_excel('base.xlsx')

# Criar a coluna 'Nome Completo'
df_base['Nome Completo'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']

# Definir a coluna 'Status' baseada na coluna 'Last Sign In [READ ONLY]'
df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVADO')

# Preparar as colunas de saída
colunas_saida = ['Nome Completo', 'Email Address [Required]', 'Status']
if 'Org Unit Path [Required]' in df_base.columns:
    colunas_saida.append('Org Unit Path [Required]')

# Ajustar o DataFrame base para incluir somente as colunas desejadas
df_base = df_base[colunas_saida]

# Função para remover caracteres especiais e acentos
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

# Função para gerar e-mail a partir do nome
def gerar_email(partes, emails_gerados, dominio='semed.limoeirodoajuru.pa.gov.br'):
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    # Remover acentos das partes do nome antes de usar no e-mail
    partes_email = [remover_acentos(parte).lower() for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    email = f"{partes_email[0]}.{partes_email[-1]}@{dominio}"
    if email not in emails_gerados:
        return email
    for parte in partes_email[1:-1]:
        email_intermediario = f"{partes_email[0]}.{parte}@{dominio}"
        if email_intermediario not in emails_gerados:
            return email_intermediario
    sufixo = 1
    email_base = f"{partes_email[0]}.{partes_email[-1]}"
    while f"{email_base}{sufixo}@{dominio}" in emails_gerados:
        sufixo += 1
    return f"{email_base}{sufixo}@{dominio}"

# Conjunto para armazenar e-mails gerados
emails_gerados = set(df_base['Email Address [Required]'].tolist())

# Carregar a planilha de teste
df_teste = pd.read_excel('teste.xlsx')

# Função para verificar e criar e-mails
def verificar_e_criar_email(nome):
    # Remover acentos e converter para minúsculas para comparação
    nome_sem_acentos = remover_acentos(nome).lower()
    nome_comparacao = df_base['Nome Completo'].apply(lambda x: remover_acentos(x).lower())
    if nome_sem_acentos in nome_comparacao.values:
        return df_base[nome_comparacao == nome_sem_acentos]
    else:
        partes = nome.split()
        email = gerar_email(partes, emails_gerados)
        emails_gerados.add(email)
        novo_usuario = {'Nome Completo': nome, 'Email Address [Required]': email}
        # Adiciona campos vazios para colunas adicionais se existirem
        for coluna in colunas_saida[2:]:
            novo_usuario[coluna] = None
        return pd.DataFrame([novo_usuario])


# Aplicar a função aos nomes na planilha de teste e concatenar resultados
resultados = df_teste['Nome'].apply(verificar_e_criar_email)
df_resultado_final = pd.concat(resultados.tolist(), ignore_index=True)

# Salvar o DataFrame em um arquivo Excel
df_resultado_final.to_excel('criação de contas.xlsx', index=False)

# Exibir ou salvar o resultado final
print(df_resultado_final)

#print("Arquivo 'criação de contas.xlsx' criado com sucesso.")
