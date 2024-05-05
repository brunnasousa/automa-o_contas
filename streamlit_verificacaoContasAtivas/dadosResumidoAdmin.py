import streamlit as st
import pandas as pd

# Função para processar os dados e criar o arquivo Excel
def process_data(df_base):
    # Combinar as colunas 'First Name [Required]' e 'Last Name [Required]' para formar o nome completo
    df_base['Full Name'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']

    # Definir o status baseado em 'Last Sign In [READ ONLY]'
    df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVO')

    # Selecionar as colunas relevantes para o novo arquivo Excel
    columns_to_include = ['Full Name', 'Email Address [Required]', 'Status']
    if 'Org Unit Path [Required]' in df_base.columns:
        columns_to_include.append('Org Unit Path [Required]')

    df_final = df_base[columns_to_include]

    return df_final

# Função para exibir as estatísticas
def display_statistics(df_base):
    # Número total de contas
    total_count = df_base.shape[0]

    # Contagem e porcentagem por Status
    status_counts = df_base['Status'].value_counts()
    status_percentage = (status_counts / total_count) * 100

    # Exibir os resultados de forma formatada
    st.subheader("1 - Contagem e Porcentagem de Status Geral:")
    st.write(f"ATIVO: {status_counts.get('ATIVO', 0)} = {status_percentage.get('ATIVO', 0):.2f}%")
    st.write(f"DESATIVADO: {status_counts.get('DESATIVADO', 0)} = {status_percentage.get('DESATIVADO', 0):.2f}%")
    st.write(f"TOTAL: {total_count} = 100.00%")

    # Verificar se a coluna 'Org Unit Path [Required]' existe para calcular as porcentagens
    if 'Org Unit Path [Required]' in df_base.columns:
        # 2 - Quantitativo e porcentagens por Org Unit Path [Required]
        org_unit_counts = df_base['Org Unit Path [Required]'].value_counts()
        org_unit_percentage = (org_unit_counts / total_count) * 100

        st.subheader("2 - Contagem e Porcentagem por Org Unit Path:")
        for path, count in org_unit_counts.items():
            st.write(f"{path}: {count} = {org_unit_percentage[path]:.2f}%")
        st.write(f"TOTAL: {total_count} = 100.00%")

        # 3 - Quantitativos e porcentagens por status em cada Org Unit Path [Required]
        org_status_counts = df_base.groupby('Org Unit Path [Required]')['Status'].value_counts().unstack(fill_value=0)
        org_status_percentage = (org_status_counts.T / org_status_counts.sum(axis=1)).T * 100

        st.subheader("3 - Contagem e Porcentagem de Status por Org Unit Path:")
        for path, row in org_status_counts.iterrows():
            st.write(f"\nOrg Unit Path [Required] = {path}")
            for status in row.index:
                st.write(f"{status}: {row[status]} = {org_status_percentage.loc[path, status]:.2f}%")
            st.write(f"TOTAL: {org_status_counts.loc[path].sum()} = 100.00%")

# Layout do Streamlit
st.title('Análise de Status de Emails')

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Upload sua base de dados:", type=['xlsx'])

if uploaded_file is not None:
    # Ler o arquivo Excel
    df_base = pd.read_excel(uploaded_file)

    # Processar os dados e criar o arquivo Excel
    df_final = process_data(df_base)

    # Exibir estatísticas
    display_statistics(df_base)

    # Download do arquivo Excel final
    excel_data = df_final.to_excel(index=False)
    st.download_button(label="📥 Download Excel", data=excel_data, file_name="usuarios_filtrados.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
