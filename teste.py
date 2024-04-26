import pandas as pd
import unicodedata

# Configurações iniciais
dominio_padrao = 'dominio.exemplo.com'
dominio_professor = 'docente.' + dominio_padrao
dominio_aluno = 'aluno.' + dominio_padrao

# Caminhos organizacionais
org_padrao = '/Servidores'
org_professor = '/Servidores'
org_alunos = '/Alunos'

# Carregar a base de dados - Google
df_base = pd.read_excel('base.xlsx')

# Planilha com os dados de entrada
df_teste = pd.read_excel('teste.xlsx')

# Criar a coluna 'Nome Completo'
df_base['Nome Completo'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']

# Definir a coluna 'Status' baseada na coluna 'Last Sign In [READ ONLY]'
df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVADO')

# Preparar as colunas de saída
colunas_saida = ['Nome Completo', 'Email Address [Required]', 'Status', 'Org Unit Path [Required]']

# Ajustar o DataFrame base para incluir somente as colunas desejadas
df_base = df_base[colunas_saida]

# Conjunto para armazenar e-mails gerados
emails_gerados = set(df_base['Email Address [Required]'].tolist())

# Função para remover caracteres especiais e acentos
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

# Função para gerar e-mail a partir do nome e tipo
def gerar_email(partes, emails_gerados, tipo='RESTO'):
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    partes_email = [remover_acentos(parte).lower() for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    
    dominio = dominio_professor if tipo == 'PROFESSOR' else dominio_aluno if tipo == 'ALUNO' else dominio_padrao

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

# Verificar a existência da coluna "Tipo" na planilha de teste
coluna_tipo = 'Tipo' in df_teste.columns

# Função para verificar e criar e-mails e definir caminhos organizacionais
def verificar_e_criar_email(nome, tipo=None):
    nome_formatado = remover_acentos(nome).title()
    nome_sem_acentos = nome_formatado.lower()
    nome_comparacao = df_base['Nome Completo'].apply(lambda x: remover_acentos(x).lower())
    
    if nome_sem_acentos in nome_comparacao.values:
        usuario_existente = df_base[nome_comparacao == nome_sem_acentos].iloc[0].to_dict()
        usuario_existente['Org Unit Path [Required]'] = org_professor if tipo == 'PROFESSOR' else org_alunos if tipo == 'ALUNO' else org_padrao
        return usuario_existente
    else:
        partes = nome_formatado.split()
        email = gerar_email(partes, emails_gerados, tipo)
        emails_gerados.add(email)
        org_path = org_professor if tipo == 'PROFESSOR' else org_alunos if tipo == 'ALUNO' else org_padrao
        novo_usuario = {
            'Nome Completo': nome_formatado,
            'Email Address [Required]': email,
            'First Name [Required]': partes[0],
            'Last Name [Required]': ' '.join(partes[1:]),
            'Org Unit Path [Required]': org_path,
        }
        return novo_usuario

# Processar os nomes na planilha de teste e criar e-mails
resultados = []
for _, row in df_teste.iterrows():
    tipo_usuario = str(row['Tipo']).strip().upper() if coluna_tipo and not pd.isna(row['Tipo']) else None
    resultado = verificar_e_criar_email(row['Nome'], tipo=tipo_usuario)
    resultados.append(resultado)

# Criar o DataFrame final
df_resultado_final = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo Excel
df_resultado_final.to_excel('criação de contas.xlsx', index=False)

print("Arquivo 'criação de contas.xlsx' criado com sucesso.")
print(df_resultado_final)
