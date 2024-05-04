
## 🤖 divisaoOrgUnitPath_2grupos

Código para separar em 2 grupos a 'Org Unit Path', e calcular a quantidade/porcentagem de ativos/desativados.

<h3>Necessário: </h3>

1. df_base = Base de Dados (Google Admin) completa com a Org Unit Path
ex: df_base = pd.read_excel('base.xlsx')

2. grupo1_nome = Grupo principal
ex: grupo1_nome = '/ALUNOS'

<h3> Explicação do código: </h3>

1 . Como é fornecido a base de dados completa do admin, ele vai separar em 2 grupos:
ex: Alunos, Servidores, Professores( Org 1 + Org 2 + Org 3)

<h2 align="center">
    <img alt="readme: base baixada do google admin" title="readme-base" src="./imgs/base-googleadmin.png" />
</h2>


2. Definir qual era o grupo principal, para poder deixar o resto como segundo grupo:
ex: Alunos, Servidores, Professores
ao dizer que o grupo 1 = "Alunos", o grupo 2 automaticamente vai ser o resto = "Servidores" e "Professores".


<h2 align="center">
    <img alt="readme: separacao por grupo 1 e grupo 2" title="readme-groups" src="./imgs/explicacao-grupos.png" />
</h2>

<h3> Explicação do Problema: </h3>

As vezes tenho várias organizações (Org Unit Path: /Alunos, /Servidores, /Professores), e preciso separar os alunos do restante.

Então determino tem será o grupo 1, e o resto da organização se chamarar grupo 2.

O código separa esses 2 grupos e me mostra a quantidade e a porcentagem com base na separação desses 2 grupos.

<h3> Retorno: </h3>

Ele retorna no terminal o resultado dessa separação


<h2 align="center">
    <img alt="readme: separacao por grupo 1 e grupo 2" title="readme-groups" src="./imgs/retorno-divisaoOrgUnitPath_2grupos.png" />
</h2>
obs: nesse exemplo não tinha /alunos