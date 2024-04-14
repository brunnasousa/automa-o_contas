"""
Aqui é fornecido uma lista de email atraves do arquivo __.xlsx (o que foi baixado do google admin)
ele junta First Name [Required] + Last Name [Required] = Full Name
Email Address [Required] na coluna B
Status = ATIVO ou DESATIVO 
e se tiver Org Unit Path [Required] ele adiciona

por fim cria um arquivo novo com esses 4 dados/colunas

----
como bonus ainda da porcentagem e quantidade de usuarios, por grupo, ativos ou desativados e afins

"""


import pandas as pd

# Carregar os dados do arquivo Excel
df_base = pd.read_excel('User_Download_13042024_215248.xlsx')




# Combinar as colunas 'First Name [Required]' e 'Last Name [Required]' para formar o nome completo
df_base['Full Name'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']

# Definir o status baseado em 'Last Sign In [READ ONLY]'
df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVO')

# Selecionar as colunas relevantes para o novo arquivo Excel
columns_to_include = ['Full Name', 'Email Address [Required]', 'Status']
if 'Org Unit Path [Required]' in df_base.columns:
    columns_to_include.append('Org Unit Path [Required]')

df_final = df_base[columns_to_include]

# Caminho para o novo arquivo Excel
output_file_path = 'usuarios_filtrados.xlsx'

# Exportar o DataFrame final para um novo arquivo Excel
df_final.to_excel(output_file_path, index=False)

print(f'O arquivo "{output_file_path}" foi criado com sucesso.')

# Número total de contas
total_count = df_base.shape[0]

# Contagem e porcentagem por Status
status_counts = df_base['Status'].value_counts()
status_percentage = (status_counts / total_count) * 100

# Exibir os resultados de forma formatada
print("----------------------")
print("1 - Contagem e Porcentagem de Status Geral:")
print(f"ATIVO: {status_counts.get('ATIVO', 0)} = {status_percentage.get('ATIVO', 0):.2f}%")
print(f"DESATIVADO: {status_counts.get('DESATIVADO', 0)} = {status_percentage.get('DESATIVADO', 0):.2f}%")
print(f"TOTAL: {total_count} = 100.00%")

# Verificar se a coluna 'Org Unit Path [Required]' existe para calcular as porcentagens
if 'Org Unit Path [Required]' in df_base.columns:
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
