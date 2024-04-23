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

# Configurações iniciais
dominio_padrao = 'dominio.exemplo.com'
dominio_professor = 'docente.' + dominio_padrao
dominio_aluno = 'aluno.' + dominio_padrao

# Carregar a base de dados - Google
df_base = pd.read_excel('base.xlsx')

# Planilha com os dados de entrada
df_teste = pd.read_excel('teste.xlsx')


############################################################################################################################
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

# Função para gerar e-mail a partir do nome e tipo
def gerar_email(partes, emails_gerados, tipo='RESTO'):
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    partes_email = [remover_acentos(parte).lower() for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    
    # Garantir que 'tipo' é uma string antes de converter para maiúsculas
    tipo = str(tipo).upper()

    # Definir o domínio de acordo com o tipo
    dominio = dominio_padrao
    if tipo == 'PROFESSOR':
        dominio = dominio_professor
    elif tipo == 'ALUNO':
        dominio = dominio_aluno
    
    # Gerar e-mail
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

# Carregar a planilha de teste e verificar a existência da coluna "Tipo"
coluna_tipo = 'Tipo' in df_teste.columns

# Função para verificar e criar e-mails e dividir os nomes
def verificar_e_criar_email(nome, tipo=None):
    # Remover acentos e converter para minúsculas para comparação
    nome_formatado = remover_acentos(nome).title()
    nome_sem_acentos = nome_formatado.lower()
    nome_comparacao = df_base['Nome Completo'].apply(lambda x: remover_acentos(x).lower())
    
    if nome_sem_acentos in nome_comparacao.values:
        usuario_existente = df_base[nome_comparacao == nome_sem_acentos].iloc[0].to_dict()
        usuario_existente['Tipo'] = tipo if tipo else None
        return usuario_existente
    else:
        partes = nome_formatado.split()
        first_name = partes[0]  # Já formatado anteriormente
        last_name = ' '.join(partes[1:]) if len(partes) > 1 else ''
        email = gerar_email(partes, emails_gerados, tipo)
        emails_gerados.add(email)
        novo_usuario = {
        'Nome Completo': nome_formatado,
        'Email Address [Required]': email,
        'First Name [Required]': first_name,
        'Last Name [Required]': last_name
    }
    # Apenas adicione o tipo se ele não for None ou 'RESTO'
    if tipo and tipo.upper() != 'RESTO':
        novo_usuario['Tipo'] = tipo
    return novo_usuario

# Processar os nomes na planilha de teste e criar e-mails
resultados = []
for _, row in df_teste.iterrows():
    # Certifique-se de que o 'tipo' seja None se a célula estiver vazia ou seja 'RESTO'
    tipo_usuario = None
    if coluna_tipo:
        tipo_usuario = str(row['Tipo']).strip().upper() if not pd.isna(row['Tipo']) and row['Tipo'].strip().upper() != 'RESTO' else None
    resultado = verificar_e_criar_email(row['Nome'], tipo=tipo_usuario)
    resultados.append(resultado)

# Criar o DataFrame final
df_resultado_final = pd.DataFrame(resultados)

# Certifique-se de que as colunas estão na ordem correta
ordem_colunas = df_base.columns.tolist() + ['Tipo', 'First Name [Required]', 'Last Name [Required]'] if coluna_tipo else df_base.columns.tolist()
df_resultado_final = df_resultado_final[ordem_colunas]

# Salvar o DataFrame em um arquivo Excel
df_resultado_final.to_excel('criação de contas.xlsx', index=False)

print("Arquivo 'criação de contas.xlsx' criado com sucesso.")

# Exibir ou salvar o resultado final
print(df_resultado_final)

