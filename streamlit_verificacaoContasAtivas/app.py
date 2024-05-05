#streamlit run app.py   
import streamlit as st
import os

# Função para executar o conteúdo de um arquivo Python
def execute_python_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    exec(code, globals())

# Listando os arquivos disponíveis
file_names = ['verificacaoContasAtivas.py', 'dadosResumidoAdmin.py', 'divisaoOrgUnitPath_2grupos.py', 'relatorio.py', 'verificacaoContasAtivas.py']
selected_file = st.sidebar.radio("Selecione um arquivo:", file_names, key="radio")

# Execução do código do arquivo selecionado
if selected_file == 'streamlit_verificacaoContasAtivas/verificacaoContasAtivas.py':
    execute_python_file(selected_file)
else:
    file_path = os.path.join('path/para/os/seus/arquivos', selected_file)  # Substitua 'path/para/os/seus/arquivos' pelo diretório onde estão seus arquivos Python
    execute_python_file(file_path)
