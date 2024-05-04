## 🤖  dadosResumidoAdmin

Caso queira somente o Nome, Email, Staus e Org de uma planilha do Google Admin


<h3> Necessario: </h3>
1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
df_base = pd.read_excel('base.xlsx')


<h3> Explicação do código/Retorno: </h3>

1 . É fornecido a base de dados completa do admin

2 . Ele faz a junção dos Nomes e também indica o Status (Ativo ou Desativado)

3. Retorna um arquivo xslx
ex: output_file_path = 'usuarios_filtrados.xlsx'

![planilha usuarios_filtrados.xlsx](/imgs/usuariosFiltrados.png)

4. Também retorna do Terminal 
	3.1 Contagem e Porcentagem de Status Geral
	3.2 Contagem e Porcentagem por Org Unit Path
	3.3 Contagem e Porcentagem de Status por Org Unit Path

![Terminal.xlsx](/imgs/terminal-DadosResumidoAdmin.png)


<h3> Explicação do Problema: </h3>

xxxxx
