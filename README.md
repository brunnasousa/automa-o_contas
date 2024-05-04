
## 🤖 divisaoOrgUnitPath_2grupos

Código para separar em 2 grupos a 'Org Unit Path', e calcular a quantidade/porcentagem de ativos/desativados.

<h3>Necessário: </h3>

1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
ex: df_base = pd.read_excel('base.xlsx')

2. grupo1_nome = Grupo principal
ex: grupo1_nome = '/ALUNOS'

Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/divisaoOrgUnitPath_2grupos.md)

![terminal apos executar o codigo](/imgs/retorno-divisaoOrgUnitPath_2grupos.png)

## 🤖 criacaoDeContas

Código para criar novos usuários


<h3> Necessario: </h3>
1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
df_base = pd.read_excel('base.xlsx')

2. df_teste = com Nome e Tipo (professor, aluno)
ex: df_teste = pd.read_excel('teste.xlsx')

3. Dizer o dominio padrão
ex: dominio_padrao = 'dominio.exemplo.com'

Para mais explicações = [divisaoOrgUnitPath_2grupos](./ExplicacaoDetalhadaDosCodigos/criacaoDeContas.md)

![planilha criação de contas.xlsx](/imgs/planilha-criacaodecontas.png)