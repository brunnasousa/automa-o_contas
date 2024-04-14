"""
Aqui é fornecido uma lista de email atraves do arquivo conta.xlsx

Vai ser separado por 2 grupos... ex: 
Alunos e Servidores( Org 1 + Org 2 + Org 3)

1 - vai me dizer a quantidade, porcentagem, quantos ativos em cada grupo 
"""

import pandas as pd

# Carregar a base de dados
df_base = pd.read_excel('base.xlsx')

# Listar valores únicos na coluna 'Org Unit Path [Required]'
print("Valores únicos em 'Org Unit Path [Required]':")
print(df_base['Org Unit Path [Required]'].unique())

# Definir o status baseado no 'Last Sign In [READ ONLY]'
df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(
    lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVO'
)

# Definindo grupos de Org Unit Path [Required]
grupo1_nome = '/Administrativo'  # Usar o nome real conforme os valores únicos
df_base['Grupo'] = df_base['Org Unit Path [Required]'].apply(
    lambda x: grupo1_nome if isinstance(x, str) and x.strip() == grupo1_nome else 'Outros'
)

# Análise agregada por grupo
total_count = df_base.shape[0]
grupo_counts = df_base['Grupo'].value_counts()
grupo_percentage = (grupo_counts / total_count) * 100

print("----------------------")
print("Contagem e Porcentagem por Grupo:")
for grupo, count in grupo_counts.items():
    print(f"{grupo}: {count} = {grupo_percentage[grupo]:.2f}%")
print(f"TOTAL: {total_count} = 100.00%")

# Análise de status dentro de cada grupo
grupo_status_counts = df_base.groupby('Grupo')['Status'].value_counts().unstack(fill_value=0)
grupo_status_percentage = (grupo_status_counts.T / grupo_status_counts.sum(axis=1)).T * 100

print("----------------------")
print("Contagem e Porcentagem de Status por Grupo:")
for grupo, row in grupo_status_counts.iterrows():
    print(f"\n{grupo}:")
    for status in row.index:
        print(f"{status}: {row[status]} = {grupo_status_percentage.loc[grupo, status]:.2f}%")
    print(f"TOTAL: {grupo_status_counts.loc[grupo].sum()} = 100.00%")
