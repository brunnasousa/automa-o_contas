
## 🤖 criacaoDeContas

Código para criar novos usuários


<h3> Necessario: </h3>
1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
df_base = pd.read_excel('base.xlsx')

2. df_teste = com Nome e Tipo (professor, aluno)
ex: df_teste = pd.read_excel('teste.xlsx')

3. Dizer o dominio padrão
ex: dominio_padrao = 'dominio.exemplo.com'


<h3> Explicação do código:</h3>

1 . É fornecido a base de dados completa do admin

2 . É fornecido a listagem com o nome para ele verificar

![planilha criação de contas.xlsx](/imgs/teste-criacaoDeContas.png)


3. Caso a pessoa já exista: Retorna se esta ativo ou não

4. Caso a pessoa não exista: cria o email com base no dominio e tipo 


<h3> Explicação do Problema: </h3>

xxxxx

<h3> Retorno: </h3>


![planilha criação de contas.xlsx](/imgs/planilha-criacaodecontas.png)
![Terminal](/imgs/terminal-criacaodecontas.png)