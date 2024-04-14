"""
Aqui é fornecido uma lista de email atraves do arquivo base.xlsx

1 - preciso saber o numero total de contas, quantas estao ativas, e quantas estao desativadas e suas respectivas porcentagens.

2 - quero saber a Org Unit Path [Required], nome e o quantitativo deles e a porcentagem

3 - por fim preciso que pegue o status dessa conta junto com a Org Unit Path [Required], e me diga a quantidade e a porcentagem delas.

ex: Org Unit Path [Required] = /Professoes
ATIVOS = 5 = 10%
DESATIVADOS = 8 = 15%
TOTAL = 13

Org Unit Path [Required] = /Alunos
ATIVOS = 5 = 10%
DESATIVADOS = 8 = 15%
TOTAL = 13

"""


import pandas as pd

# Carregar a base de dados
df_base = pd.read_excel('base.xlsx')

# Função para definir o status baseado no 'Last Sign In [READ ONLY]'
df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(
    lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVO'
)

# 1 - Número total de contas, quantas estão ativas e desativadas, e suas respectivas porcentagens
total_count = df_base.shape[0]
status_counts = df_base['Status'].value_counts()
status_percentage = (status_counts / total_count) * 100

# Exibir os resultados de forma formatada
print("----------------------")
print("1 - Contagem e Porcentagem de Status Geral:")
# Imprimir ATIVO primeiro, depois DESATIVADO
print(f"ATIVO: {status_counts.get('ATIVO', 0)} = {status_percentage.get('ATIVO', 0):.2f}%")
print(f"DESATIVADO: {status_counts.get('DESATIVADO', 0)} = {status_percentage.get('DESATIVADO', 0):.2f}%")
print(f"TOTAL: {total_count} = 100.00%")

# 2 - Quantitativo e porcentagens por Org Unit Path [Required]
org_unit_counts = df_base['Org Unit Path [Required]'].value_counts()
org_unit_percentage = (org_unit_counts / total_count) * 100

print("----------------------")
print("2 - Contagem e Porcentagem por Org Unit Path:")
for path, count in org_unit_counts.items():
    print(f"{path}: {count} = {org_unit_percentage[path]:.2f}%")
print(f"TOTAL: {total_count} = 100.00%")

# 3 - Quantitativos e porcentagens por status em cada Org Unit Path [Required]
org_status_counts = df_base.groupby('Org Unit Path [Required]')['Status'].value_counts().unstack(fill_value=0)
org_status_percentage = (org_status_counts.T / org_status_counts.sum(axis=1)).T * 100

print("----------------------")
print("3 - Contagem e Porcentagem de Status por Org Unit Path:")
for path, row in org_status_counts.iterrows():
    print(f"\nOrg Unit Path [Required] = {path}")
    for status in row.index:
        print(f"{status}: {row[status]} = {org_status_percentage.loc[path, status]:.2f}%")
    print(f"TOTAL: {org_status_counts.loc[path].sum()} = 100.00%")