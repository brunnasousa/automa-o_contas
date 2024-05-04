## 🤖  verificacaoContasAtivas

Fornecemos uma lista de email e ele retorna o status (ativo ou desativado)


<h3> Necessario: </h3>
1. base_data_path = Base de Dados (Google Admin)
base_data_path = 'limoeiro teste.xlsx'

2. emails_to_check_path = Lista dos emails para verificar
ex: emails_to_check_path = 'conta.xlsx'


<h3> Explicação do código/Retorno: </h3>

1 . É fornecido a base de dados completa do admin

2 . Ele faz a verificaçao dos emails atraves da planilha fornecida 

3. Retorna um arquivo xslx
ex: output_file_path = 'Status_email.xlsx'

![planilha Status_email.xlsx](/imgs/retorno-verificacaoAtivos.png)

4. Também retorna do Terminal 
	3.1 emails_to_check_path = 'conta.xlsx'

* Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/verificacaoContasAtivas.md)



## 🤖  dadosResumidoAdmin

Caso queira somente o Nome, Email, Staus e Org de uma planilha do Google Admin


<h3> Necessario: </h3>
1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
df_base = pd.read_excel('base.xlsx')


![planilha usuarios_filtrados.xlsx](/imgs/usuariosFiltrados.png)

* Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/dadosResumidoAdmin.md)

## 🤖 divisaoOrgUnitPath_2grupos

Código para separar em 2 grupos a 'Org Unit Path', e calcular a quantidade/porcentagem de ativos/desativados.

<h3>Necessário: </h3>

1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
ex: df_base = pd.read_excel('base.xlsx')

2. grupo1_nome = Grupo principal
ex: grupo1_nome = '/ALUNOS'

* Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/divisaoOrgUnitPath_2grupos.md)


## 🤖 criacaoDeContas

Código para criar novos usuários


<h3> Necessario: </h3>
1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
df_base = pd.read_excel('base.xlsx')

2. df_teste = com Nome e Tipo (professor, aluno)
ex: df_teste = pd.read_excel('teste.xlsx')

3. Dizer o dominio padrão
ex: dominio_padrao = 'dominio.exemplo.com'


![planilha criação de contas.xlsx](/imgs/planilha-criacaodecontas.png)

* Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/criacaoDeContas.md)