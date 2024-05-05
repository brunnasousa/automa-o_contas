#pip install pandas plotly streamlit openpyxl xlsxwriter
import pandas as pd
import plotly.express as px
import streamlit as st
from io import BytesIO
from datetime import date

def check_status(email, df_base):
    match = df_base[df_base['Email Address [Required]'] == email]['Last Sign In [READ ONLY]']
    if not match.empty:
        return 'DESATIVADO' if match.iloc[0] == 'Never logged in' else 'ATIVADA'
    else:
        return 'EMAIL NÃO ENCONTRADO'

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
        # Adicionando a data atual ao título da coluna de status
        today = date.today().strftime("%d/%m/%Y")
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']  # Nome da planilha pode mudar, ajuste conforme necessário
        worksheet.write(0, df.shape[1] - 1, f"Status {today}")  # A última coluna é onde está a coluna de status

    processed_data = output.getvalue()
    return processed_data


# Layout do Streamlit
st.title('Análise de Status de Emails')

# Upload de arquivos
base_data_file = st.file_uploader("Upload sua base de dados:", type=['xlsx'])
emails_to_check_file = st.file_uploader("Upload a lista de emails para verificar:", type=['xlsx'])

if base_data_file and emails_to_check_file:
    df_base = pd.read_excel(base_data_file)
    df_emails_to_check = pd.read_excel(emails_to_check_file)

    email_column = df_emails_to_check.columns[0]
    df_emails_to_check['Status'] = df_emails_to_check[email_column].apply(lambda email: check_status(email, df_base))

    status_counts = df_emails_to_check['Status'].value_counts()
    total_emails = df_emails_to_check.shape[0]
    status_percentage = (status_counts / total_emails) * 100

    # Incluir a linha 'TOTAL'
    status_counts['TOTAL'] = total_emails
    status_percentage['TOTAL'] = 100  # O total é sempre 100% do total

    # Criação de um DataFrame para apresentação
    summary_df = pd.DataFrame({
        'Status': status_counts.index,
        'qtd': status_counts.values,
        'percentagem': status_percentage.values
    })

    # Apresentação dos dados com st.dataframe
    st.markdown("### Resultado:")
    st.dataframe(summary_df.style.format({'percentagem': "{:.1f} %"}))
    # Organizando gráficos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Quantitativo de Status')
        fig_quant = px.bar(status_counts.drop('TOTAL'), title="Quantidade por Status")
        st.plotly_chart(fig_quant, use_container_width=True)

    with col2:
        st.subheader('Porcentagem de Status')
        fig_perc = px.pie(values=status_percentage, names=status_percentage.index, title="Porcentagem por Status")
        st.plotly_chart(fig_perc, use_container_width=True)

    # Tabela de dados
    st.subheader('Status dos Emails')
    st.write(df_emails_to_check[[email_column, 'Status']])

    # Download de Excel
    excel_data = convert_df_to_excel(df_emails_to_check[[email_column, 'Status']])
    st.download_button(label="📥 Download Excel",
                       data=excel_data,
                       file_name="status_emails.xlsx",
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
