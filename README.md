# Introbattle 2

Introbattle 2 é um jogo simulador de batalha em turnos feito em pygame. É pra se divertir!

## Como iniciar?

Se já não estiver instalado no seu computador, é necessário ter o Pygame.

```bash
pip install pygame
```
Agora, basta executar a main no terminal (dentro do diretório onde estão os arquivos .py do jogo).

```bash
python3 main.py
```

Tudo pronto.
## Sobre o jogo
O jogo acontece por uma série de 12 rounds. Neles você deve derrotar todos os inimigos antes que eles _derrotem você_. Se todos os seus aliados morrerem, você perde e volta no round 1.

Para te auxiliar durante as batalhas, você deve comprar os lutadores (ou monstros) no menu principal, analisando os status e skills e selecionando aqueles que mais combinam com a estratégia que você está formando.

Além dos lutadores, você também pode comprar cartas e adicioná-las ao seu deck. Cartas são itens de efeitos diversos que podem ser ativados durante o curso das batalhas.

Derrotar inimigos te garantirá mais dinheiro para aprimorar os membros da sua equipe e adquirir mais cartas!

A cada 3 rounds, você batalhará contra um boss, então economize seus recursos para poder vencê-lo e progredir.

O jogo adota o sistema **Press Turn** simplificado, ou seja, você deve administrar as ações da sua equipe estrategicamente para atingir seus objetivos. Atingir um crítico **pode** (atenção no **_pode_**) te garantir mais turnos, e errar um ataque te fará perder mais ações.

Ferramentas importantes :
**Modo informação** - durante a batalha, segurar o botão direto do mouse ativará o modo informação. Colocar o cursor do mouse sobre um monstro ou uma carta revelará suas status (como nome, vida, ataque, custo, etc.)
**Passar a vez** - nesse sistema, passar a vez só te faz perder "meio" turno, use essa opção para se reorganizar.

## Sobre o código
O jogo foi desenvolvido em intervalos curtos de uma hora diária por um _iniciante_ em programação, então **por favor** não repare na bagunça.

## Ainda há muito a ser feito

Um dos principais objetivos atuais é tornar o código o mais otimizado e leve possível (o jogo possui performance estável mas quedas na taxa de quadros podem acontecer).
Efeitos sonoros estão completamente ausentes.

